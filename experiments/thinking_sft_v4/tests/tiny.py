"""Tiny offline stand-ins for Qwen3-0.6B: a byte-level BPE tokenizer with a Qwen3-like ChatML template and a
randomly initialized Qwen3ForCausalLM. Shared by the SFT tests and the generator tests (stable API):

    build_tiny_tokenizer() -> PreTrainedTokenizerFast   (the eight contract tags NOT added yet)
    build_tiny_model(tokenizer, attn='sdpa', seed=0, rows=None) -> Qwen3ForCausalLM (fp32, eval mode)

Like Qwen3: <|endoftext|> is pad, <|im_end|> is eos, <|im_start|>/<|im_end|> are special, <think>/</think> are
added non-special tokens, digits are split one per token by the pre-tokenizer, and the embedding matrix has
more rows than the tokenizer so the eight tags fit without a resize (unless rows is given).
"""
import torch
from tokenizers import AddedToken, Regex, Tokenizer, decoders, models, pre_tokenizers, trainers
from transformers import PreTrainedTokenizerFast, Qwen3Config, Qwen3ForCausalLM

# Qwen2/Qwen3 pre-tokenizer split pattern (digits one at a time).
QWEN_SPLIT = (r"(?i:'s|'t|'re|'ve|'m|'ll|'d)|[^\r\n\p{L}\p{N}]?\p{L}+|\p{N}| ?[^\s\p{L}\p{N}]+[\r\n]*|"
              r"\s*[\r\n]+|\s+(?!\S)|\s+")
SPECIAL = ['<|endoftext|>', '<|im_start|>', '<|im_end|>']
THINK = ['<think>', '</think>']
# Minimal Qwen3-like template: with enable_thinking=False an empty think block is prefilled.
CHAT_TEMPLATE = (
    "{% for message in messages %}<|im_start|>{{ message['role'] }}\n{{ message['content'] }}<|im_end|>\n"
    "{% endfor %}{% if add_generation_prompt %}<|im_start|>assistant\n"
    "{% if enable_thinking is defined and enable_thinking is false %}<think>\n\n</think>\n\n{% endif %}"
    "{% endif %}")
CORPUS = [
    'Solve the problem. Let x be a real number such that x + 2 = 5. Find x.',
    'We decompose the problem into cases and candidates, then verify each method.',
    'branches= branches=2 branches=3 branches=4',
    'Parallel Path Summary Plan parallel path summary plan',
    '<Parallel> </Parallel> <Path> </Path> <Summary> </Summary> <Plan> </Plan>',
    'decompose cases candidates methods verify',
    '1: first case 2: second case 3: third case 4: fourth case',
    'The answer is 42. Therefore the final answer is \\boxed{3}.',
    'Compute the sum 1 + 2 + 3 + 4 = 10, so the total is 10 and the product is 24.',
    'If x > 0 then f(x) = x, otherwise f(x) = -x. Both branches agree on the summary.',
    'Okay, let me think step by step about this question and check the result again.',
    'Hmm, wait. Let us double check: 3 * 4 = 12 and 12 / 2 = 6.',
]


def build_tiny_tokenizer(vocab_size=480):
    tokenizer = Tokenizer(models.BPE())
    tokenizer.pre_tokenizer = pre_tokenizers.Sequence([
        pre_tokenizers.Split(Regex(QWEN_SPLIT), behavior='isolated', invert=False),
        pre_tokenizers.ByteLevel(add_prefix_space=False, use_regex=False)])
    tokenizer.decoder = decoders.ByteLevel()
    trainer = trainers.BpeTrainer(vocab_size=vocab_size, special_tokens=SPECIAL, show_progress=False,
                                  initial_alphabet=pre_tokenizers.ByteLevel.alphabet())
    tokenizer.train_from_iterator(CORPUS * 4, trainer=trainer)
    fast = PreTrainedTokenizerFast(
        tokenizer_object=tokenizer, eos_token='<|im_end|>', pad_token='<|endoftext|>',
        additional_special_tokens=['<|im_start|>', '<|im_end|>'], chat_template=CHAT_TEMPLATE,
        clean_up_tokenization_spaces=False, model_max_length=131072)
    fast.add_tokens([AddedToken(token, special=False, normalized=False) for token in THINK])
    return fast


def build_tiny_model(tokenizer, attn='sdpa', seed=0, rows=None, initializer_range=0.1):
    """rows: embedding rows; default len(tokenizer) + 8 tags rounded up to a multiple of 64, plus slack.
    initializer_range is large so that logits are far from uniform and masking mistakes are visible."""
    if rows is None:
        rows = (len(tokenizer) + 8 + 63) // 64 * 64 + 64
    config = Qwen3Config(
        vocab_size=rows, hidden_size=64, intermediate_size=128, num_hidden_layers=2, num_attention_heads=4,
        num_key_value_heads=2, head_dim=16, max_position_embeddings=4096, rope_theta=10000.0,
        rms_norm_eps=1e-6, tie_word_embeddings=True, use_sliding_window=False, sliding_window=None, initializer_range=initializer_range,
        bos_token_id=None, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.pad_token_id,
        torch_dtype='float32', attn_implementation=attn)
    torch.manual_seed(seed)
    model = Qwen3ForCausalLM(config)
    return model.float().eval()
