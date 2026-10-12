# Independent semantic review of downloaded SFT

Source: `${DATA_SOURCE_ROOT}/sft_messages_5000.jsonl`; 5000 rows; SHA-256 `ce0bc7febe267be6761d6689e52f5b57bcaaba6ebdb5a9ed7813ffea35a05dda`.

Random sampling: Python `random.Random(20261009).sample(range(5000), 30)`, preserving returned order. All row numbers are one-based. Complete quantity referents, all context relations, the query and complete assistant were read. A reversible compact reader substituted quantity IDs only to avoid repeating long referents; it preserves every relation and assistant calculation. Random source records are preserved in `realistic-semantic-random-sample.jsonl`.

This review establishes observations in 30 random rows plus 3 deliberately chosen extremes, not corpus-wide semantic proof. A zero observed error count is not a guarantee. Counts below apply only to the random 30, unless explicitly marked targeted.

## Sample counts

```json
{
  "random_n": 30,
  "parallel_rows": 27,
  "sequential_rows": 3,
  "multiple_round_rows": 22,
  "blocks": 54,
  "paths": 194,
  "operations": 689,
  "rows_with_identical_sibling_first_numeric_arithmetic": 16,
  "rows_with_duplicate_complete_sibling_numeric_chains": 3,
  "material_realism_concern_rows": 21,
  "observed_wrong_arithmetic_rows": 0,
  "observed_wrong_count_or_award_binding_rows": 0,
  "observed_leakage_rows": 0,
  "observed_irrelevant_named_path_endpoints": 0,
  "templates": {
    "teachers_in_school": 10,
    "library_collections": 9,
    "crazy_zootopia": 7,
    "movie_festival_awards": 4
  }
}
```

## Interpretation

The sample is useful supervision for discovering and scheduling a named-quantity DAG: 27/30 rows have genuinely sibling-independent required outputs, with 22/30 needing multiple dependency rounds. Later blocks begin from previously computed joins. Every examined branch endpoint contributes to the queried quantity; I found no sibling-output read, future-output read, prematurely revealed intermediate answer, wrong arithmetic, or film/award query binding error.

Distinct named quantities do not guarantee distinct computation: 16/30 repeat the identical first numerical operation in sibling paths; 3/30 duplicate a complete numerical chain (1140, 1564, 4702). These are exact printed-expression matches, not an algebraic-simplification census. Names represent distinct required outputs, so these repetitions are not automatically invalid; however some nominal width is entity duplication rather than multiple computational tasks.

All 30 use a very small arithmetic vocabulary and the same declarative relation style. Long labels, shuffled facts and many dependency edges create tracking difficulty; no sample requires rates applied to quantities, percentage interpretation, division/remainder, unit conversion, choices or constraints. Every existing Summary repeats the branch terminal labels and values plus the same boilerplate. This is concise as a linear proof relative to repeating derivations, but not compact as a natural solution.

Material realism concerns occur in 21/30: 10 school problems, 7 zoo problems, 4 film problems. School counts are numerically equated/added to per-school teacher averages and reach implausible staffing/institution magnitudes; newborns-per-adult reach hundreds or thousands without any period; one festival can have thousands of films on one narrow topic or thousands of awards. The 9 library problems have plausible book-count magnitudes and consistent count referents, but their inter-library scalar relations still lack a natural operational cause. These stipulated cross-quantity numeric relationships are not a formal arithmetic contradiction: the text explicitly defines them. Therefore I am flagging realism and generalization limitations, not asserting these answers are semantically false.

No observed row has an explicit non-numeric plan or stable local branch/quantity IDs. Adding these is a deterministic presentation transformation and does not repair narrative realism or arithmetic diversity. A plan must name dependencies and requested outputs without inserting branch values before the corresponding computation. Stable IDs should preserve quantity type and full referent in a side dictionary; blindly treating film count and award count as the same variable would be unsafe.

Recommendation: retain the current data as an auxiliary dependency-scheduling curriculum, with unchanged originals and deterministic ID/plan derivatives separately identified. If the intended SFT is realistic, varied math reasoning, generate a new primary set rather than spending a DeepSeek call merely adding tags to these rows. Give one reusable prompt an explicit varying dependency specification and realistic unit-aware constraints; validate both arithmetic and semantics after generation. Do not discard the current corpus solely from this sample.

## Per-row annotations

### Row 1637 · realistic_parallel_01636

Template `teachers_in_school`; 9 operations; critical depth 9; schedule `[]`.

Sequential 9-edge chain; no independent required sibling calculation.

1449 teachers per public high school, then 1444 medical schools; school counts and per-school averages are related as arbitrary scalars.

Evidence:
> Teachers per public high school in Northgate = 3 × 483 = 1449.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 3779 · realistic_parallel_03778

Template `library_collections`; 8 operations; critical depth 6; schedule `[2]`.

Two chains share the already established 40 cookbooks: terminal 79 mystery novels and 101 music books, joined as 180 science books.

Book counts 20..360 are plausible; inter-library numerical relations remain artificial.

Evidence:
> Architecture books at Pine Street Library = 2 × 180 = 360.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 1140 · realistic_parallel_01139

Template `library_collections`; 33 operations; critical depth 19; schedule `[3, 5, 2]`.

Three rounds require preceding joins; block 2 paths 2 and 4 repeat the entire numeric chain 220→440→880→885 under music versus mystery-book names.

Book counts including 5290 memoirs are possible; long entity labels and 33 tiny operations generate difficulty.

Evidence:
> Travel memoirs at Pine Street Library = 5302 - 12 = 5290.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 2739 · realistic_parallel_02738

Template `teachers_in_school`; 25 operations; critical depth 16; schedule `[2, 5]`.

After first join 247, sequential 494→501→496 establishes second-round input; 5 branch results join downstream.

4468 average teachers per design school; sums mix school counts and average staffing without an operational explanation.

Evidence:
> Teachers per design school in Kingsport = 4471 - 3 = 4468.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 688 · realistic_parallel_00687

Template `teachers_in_school`; 7 operations; critical depth 7; schedule `[]`.

Sequential 7-edge chain only.

796 teachers per public high school and 806 science schools; contrived count/average relations.

Evidence:
> Teachers per public high school in Glenfield City = 801 - 5 = 796.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 1579 · realistic_parallel_01578

Template `crazy_zootopia`; 15 operations; critical depth 10; schedule `[4]`.

Four independent chains from the known 13 ibex produce 39,26,5,7; all are consumed by the later sums.

39 newborns per adult deer, 33 per adult moose, 72 per adult badger; no observation period or reproductive interpretation.

Evidence:
> Newborns per adult badger at Dawn Valley = 33 + 39 = 72.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 4391 · realistic_parallel_04390

Template `movie_festival_awards`; 18 operations; critical depth 12; schedule `[2, 4]`.

Round 1 endpoints 34 films and 9 films yield 43; ×2 gives the 86 shared by round 2. No award/film identity swap.

1143 awards for films about a village festival and 1135 films on a single traveling-theater topic at a festival are implausibly large.

Evidence:
> Films about a traveling theater at Silver Screen Harbor = 1143 - 8 = 1135.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 3778 · realistic_parallel_03777

Template `movie_festival_awards`; 34 operations; critical depth 18; schedule `[5, 5]`.

Both rounds have 5 useful named outputs; several second-round chains reuse the same first arithmetic 3×173.

2234 awards on one hidden-library topic and >2000 awards on calm-road-trip/family-bakery topics are implausible in a festival story.

Evidence:
> Awards for films about a hidden library at Winterglass Cinema Forum = 2223 + 11 = 2234.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 1893 · realistic_parallel_01892

Template `teachers_in_school`; 9 operations; critical depth 9; schedule `[]`.

Sequential 9-edge chain only.

318 average teachers per music school, 636 per elementary school, final 623 per coding school; count/average mix.

Evidence:
> Teachers per coding school in Grandhaven = 625 - 2 = 623.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 777 · realistic_parallel_00776

Template `teachers_in_school`; 17 operations; critical depth 9; schedule `[5]`.

Five sibling chains from 24 staffing average; all terminal values feed later sums. First ×2 duplicated under different names.

300 average teachers per sports school and 302 history schools; artificial specialized-school network.

Evidence:
> Teachers per sports school in Stormvale = 295 + 5 = 300.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 3783 · realistic_parallel_03782

Template `library_collections`; 8 operations; critical depth 6; schedule `[2]`.

Both chains start 2×48=96 under different book names, then diverge to 87 versus 288 and both enter sum.

Book magnitudes up to 750 are plausible; 8-operation relation puzzle rather than an operational story.

Evidence:
> Fantasy novels at Cedar Point Library = 2 × 375 = 750.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 2113 · realistic_parallel_02112

Template `library_collections`; 31 operations; critical depth 17; schedule `[4, 4]`.

Round 1 includes repeated ×2→×2 under two names but last offsets differ; round 2 depends on the join and shared 916.

Book counts are plausible. +10 followed by -10 at final two language-book entities adds rote steps.

Evidence:
> Language textbooks at Harborview Library = 3689 - 10 = 3679.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 2136 · realistic_parallel_02135

Template `movie_festival_awards`; 27 operations; critical depth 17; schedule `[3, 5]`.

First-round 399,156,576 join to shared1124; second-round 5 separate offset chains feed final award total.

5584 awards for one runaway-train topic; films and awards are correctly bound but their numerical relations have no realistic mechanism.

Evidence:
> Awards for films about a runaway train at Northlight Film Week = 5581 + 3 = 5584.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 2800 · realistic_parallel_02799

Template `library_collections`; 20 operations; critical depth 14; schedule `[2, 4]`.

Genuine two rounds, but a later branch has +1,-1 cancellation; another +2,+6,-8 returns to shared1080.

Book sizes plausible; avoid equating formal graph length with irreducible calculation difficulty.

Evidence:
> Biographies at Northgate Library = 4318 - 4 = 4314.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 2466 · realistic_parallel_02465

Template `crazy_zootopia`; 28 operations; critical depth 17; schedule `[5, 3]`.

Second round starts only after 1292→1289; both rounds contribute all named endpoints.

1288 newborns per adult falcon and 1290 per adult ocelot; no time horizon, plus adult-count/average sums.

Evidence:
> Newborns per adult falcon at Riverglass Sanctuary = 1289 - 1 = 1288.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 4404 · realistic_parallel_04403

Template `teachers_in_school`; 24 operations; critical depth 16; schedule `[4, 3]`.

First 4 chains share7 and yield21,28,9,16; their joins establish150 for second3 chains.

1417 average teachers per robotics school; school count plus average staff used as bare scalar sum.

Evidence:
> Teachers per robotics school in Glenfield City = 1421 - 4 = 1417.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 3173 · realistic_parallel_03172

Template `movie_festival_awards`; 38 operations; critical depth 25; schedule `[2, 5, 3]`.

Three useful rounds with critical depth25; each new round depends on the previous join, not future outputs.

7612 films about one family bakery at a festival; >2500 awards on topic subgroups.

Evidence:
> Films about a family bakery at Muted Stories Cinema Fest = 7609 + 3 = 7612.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 3198 · realistic_parallel_03197

Template `teachers_in_school`; 26 operations; critical depth 16; schedule `[3, 5]`.

Two rounds:46,84,126→shared505, then five useful named offset chains.

2560 average teachers per design school and 2561 elementary schools; arbitrary average/count sums.

Evidence:
> Teachers per design school in Clearwater Bay = 2043 + 517 = 2560.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 3872 · realistic_parallel_03871

Template `library_collections`; 28 operations; critical depth 17; schedule `[3, 5]`.

Three first-stage chains yield201,216,88→505→495; second-stage outputs all join. Same 2×495 reused under two names.

Plausible collection sizes through4932; inflated language length, small arithmetic operators.

Evidence:
> Graphic novels at Eastbridge Library = 4926 + 6 = 4932.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 273 · realistic_parallel_00272

Template `crazy_zootopia`; 18 operations; critical depth 13; schedule `[4, 2]`.

Round 1 independent from8; sequential joins yield260 for second2 chains. Distinct chains may end at equal48 without leakage.

531 newborns per adult fox and 533 per adult penguin; adults and per-adult averages directly added.

Evidence:
> Newborns per adult fox at Pine Ridge Reserve = 533 - 2 = 531.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 4332 · realistic_parallel_04331

Template `crazy_zootopia`; 7 operations; critical depth 6; schedule `[2]`.

Small 2-branch example: known1 yields8 toucans and7 newborns-per-bison, then sum15 and final14 macaques.

15 newborns per adult snow leopard; low operation count does not rescue the unmotivated cross-unit story.

Evidence:
> Newborns per adult snow leopard at Amber Coast Zoo = 7 + 8 = 15.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 3823 · realistic_parallel_03822

Template `library_collections`; 20 operations; critical depth 14; schedule `[5, 2]`.

First5 chains from10 produce42,20,5,30,19; joined116→348 enables second branches696 and700. Same ×2 initial step repeated.

All book counts plausible; genuine multi-round dependencies but very narrow operator vocabulary.

Evidence:
> Graphic novels at Grandview Library = 1396 + 2 = 1398.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 3311 · realistic_parallel_03310

Template `teachers_in_school`; 22 operations; critical depth 14; schedule `[4, 2]`.

First4 independent chains from80; five sequential steps yield707, then two chains709 and706 are joined.

1409 average teachers per history school; arbitrary scalar equations rather than staffing totals.

Evidence:
> Teachers per history school in Northgate = 1415 - 6 = 1409.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 1652 · realistic_parallel_01651

Template `library_collections`; 28 operations; critical depth 17; schedule `[5, 3]`.

First5 chains from4, including repeated 2×4 under two names; joins yield53 for second3 chains.

Small to medium book counts up to235 are plausible; same template and tiny arithmetic chains.

Evidence:
> Poetry collections at Stonegate Library = 235 - 3 = 232.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 3692 · realistic_parallel_03691

Template `crazy_zootopia`; 34 operations; critical depth 20; schedule `[5, 3]`.

First5 chains from36; joined543 and three sequential offsets yield526 for next3 chains. Repeated3×36.

1578 newborns per adult capybara, 509 per adult panther, 526 per adult zebra.

Evidence:
> Newborns per adult capybara at Ironwood Farm = 1566 + 12 = 1578.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 3532 · realistic_parallel_03531

Template `crazy_zootopia`; 32 operations; critical depth 21; schedule `[3, 5, 2]`.

Three rounds: known32→198→204, then joined2490, then two chains2493/2504; no future result supplied before its join.

4997 newborns per adult eagle and4990 per adult ocelot; unsupported biologic interpretation.

Evidence:
> Newborns per adult eagle at Frostpine Reserve = 2504 + 2493 = 4997.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 1564 · realistic_parallel_01563

Template `library_collections`; 29 operations; critical depth 19; schedule `[5, 3]`.

First block paths2 and3 repeat full single-step 2×30=60 for music books versus engineering manuals; both named outputs are added downstream.

Book counts through2127 plausible; real variable distinctness but redundant numerical calculation and rote relation story.

Evidence:
> Architecture books at Oak Lane Library = 2121 + 6 = 2127.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 4702 · realistic_parallel_04701

Template `crazy_zootopia`; 39 operations; critical depth 22; schedule `[3, 4, 5]`.

Three useful rounds; second block paths1 and3 both compute single-step 2×147=294 under tern/heron names; sum uses both.

1327 newborns per adult moose and 1306 per adult dingo; 6585 adult lemurs at a park.

Evidence:
> Newborns per adult moose at Frostpine Reserve = 1315 + 12 = 1327.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 4308 · realistic_parallel_04307

Template `teachers_in_school`; 30 operations; critical depth 19; schedule `[4, 3, 3]`.

Three rounds; first starts with duplicated2×11 and11-7 on separate named quantities; later stages depend on their joins.

2296 technical schools and >760 average teachers per robotics/design school.

Evidence:
> Technical schools in Ashford = 2299 - 3 = 2296.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

### Row 2224 · realistic_parallel_02223

Template `teachers_in_school`; 25 operations; critical depth 14; schedule `[3, 5]`.

Two rounds; multiple sibling paths begin2×18 or2×71, but different endpoints all feed target.

1900 technical schools in one town; per-school averages summed with institution counts.

Evidence:
> Technical schools in Cedar Falls = 1901 - 1 = 1900.

Observed: arithmetic and queried count/average/award referent correct; no sibling/future leakage; all named branch outputs used.

## Deliberately targeted extremes, excluded from random counts

### Row 2622 · realistic_parallel_02621

Global maximum critical depth 30 and operation count55; schedule[5,5,5].

All 15 named path endpoints independently computable from stage-known inputs and used later; repeated 2×36 initially and +11 after third shared input; two chains reach92 by different route.

Newborns per adult zebra=5820, per adult yak=5832, final adult meerkats=29080; growing newborn averages and adult counts have no natural breeding mechanism.

> Newborns per adult zebra at Silverbrook Sanctuary = 5832 - 12 = 5820.

### Row 157 · realistic_parallel_00156

Minimum operation count13 among maximum-width5 rows, tie broken by lower depth then row number.

Five paths have useful named outputs, but two entire paths both compute13+4=17 for medical-school count and teacher-per-history-school average. Effective numerical width is smaller than named width.

Institution count and teacher-per-school average are numerically summed; magnitudes are smaller but no operational staffing relation.

> Teachers per history school in Southport = 13 + 4 = 17.

### Row 512 · realistic_parallel_00511

Near-maximum depth29 and second-largest operation count52 among schedule[5,5,5] rows.

All three stages depend on previous joins; distinct required branches but 2×114 and3×114 are repeated first steps. Third-round branch11783→11772→11783 cancels offsets.

Final58936 awards on chess-prodigy films, 58930 films about winter mystery,23563 awards on forgotten-space-colony films at one festival.

> Awards for films about a chess prodigy at Silver Screen Harbor = 58930 + 6 = 58936.

No leakage or arithmetic/query-binding defect observed in these 3 targeted rows either. Their selection cannot estimate prevalence. Width is bounded at 5 in the source metadata; the selected wide cases demonstrate genuinely distinct named outputs and repeated arithmetic under different names.
