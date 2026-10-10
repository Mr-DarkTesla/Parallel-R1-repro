import json
from collections import Counter
from pathlib import Path
p=Path(__file__).parent
rows=[json.loads(s) for s in (p/'input.jsonl').read_text().splitlines()]
# Manual judgments after reading all 50 complete responses; no reference answers used.
items=[
('error',False,True,False,'Ложная формула total=red+green-neither; выдуман overlap. Parts лишь перечисляют данные.'),
('error',False,True,True,'Сначала 0.5 часа названо дневным временем и получено 3.5 часа; исправлено позднее. Parts последовательны.'),
('error',False,True,True,'Необоснованно предполагается, что сестре отданы все оставшиеся 13; есть круговое утверждение 13 минус отданное.'),
('error',True,True,False,'Расход 1200 и остаток 80 вычислены из условия независимо, но первое объяснение пропускает страховку; длинный пересчёт и неясная цель первой ветви.'),
('weak',False,False,True,'Одна цепочка 100*6=600, затем 600*1.2; Parts данные, расчёт, результат.'),
('error',False,True,True,'В ответе утверждается 4*2^4=32; реально 64. Недельная цепочка зависима, Jane только данное.'),
('error',False,True,True,'Сначала сумма первых двух фильмов ошибочно 3 и третий 2; позднее исправлено. Третий зависит от второго.'),
('weak',False,False,True,'120 наклеек, 12 долларов, 6 долларов образуют одну зависимую цепочку.'),
('weak',False,False,True,'Part 2 использует 672 из Part 1; 500 только данное, второго независимого вычисления нет.'),
('weak',False,False,True,'25, затем 65, затем 130 вычисляются последовательно; Part 1 только 40 из условия.'),
('useful',True,False,False,'Время львов 3*2=6 и носорогов 2*2=4 независимо; затем сумма 10.'),
('weak',False,False,True,'Стоимость 45 использует ранее полученные 3 фунта.'),
('weak',True,False,False,'25 и 80 минут независимы, но первая вычисляющая их фраза тесно смешивает подготовку и обе ветви; позднее модель отрицает независимость. Консервативный отказ от тегов.'),
('weak',False,False,True,'Среда и пятница используют понедельник 60; независимые формулы из исходных 80 и 20 не записаны.'),
('weak',False,False,True,'Сначала остаток 20, затем уравнение 4O=20; проверка 15 использует найденное O.'),
('weak',True,False,True,'В основном одна сумма с переводом пятницы; десятичная проверка повторяет результат и подготовленное 1.25, Parts перечисляют данные.'),
('error',False,True,False,'Сказано half an hour is 15 minutes, затем исправлено. Первый путь только данное 30 миль.'),
('useful',True,False,False,'Скидка на билет 0.20*10=2 и комбо 0.50*10=5 независимы; сумма 7 после обеих.'),
('weak',False,False,True,'Уравнение, подстановка, Drew=36, Sam=18; Parts с условиями не отдельные вычисления.'),
('error',True,True,False,'56/4=14 и 44/4=11 независимы, но названо выполненным равенство мальчиков и девочек при 14 против 11; условие неоднозначно.'),
('weak',False,False,True,'Единственное исходное вычисление 2*23=46, затем вычитание; повторные спекуляции о потере перьев не ветви.'),
('useful',True,False,False,'Недельные количества 14,21,42 независимы после общей подготовки 6 в день; их сумма после ветвей.'),
('weak',True,False,False,'Время уборки и запас 180 независимы, но первый итог 150 уже объединён до вычисления запаса; честный блок с объединением после всех ветвей требует перестановки.'),
('weak',False,False,True,'24,48,16 последовательны; Kyle использует Mimi, Leigh использует Kyle.'),
('weak',False,False,True,'Вычисляется только 100*3=300; понедельник и среда лишь данные.'),
('useful',True,False,False,'Выручка pancakes 60*4=240 и bacon 90*2=180 независима; объединение 420 после них.'),
('error',False,True,True,'11 названо больше 12, пять простых посчитаны как четыре, получено 25%; позже исправлено на 20%.'),
('error',True,True,False,'Коэффициенты разных степеней независимы, но сказано, что первый полином имел -x³; затем много ложных рассуждений о независимости combine/simplify.'),
('error',True,True,False,'После верного раскрытия скобок сказано, что -5 становится -5 вместо +5. Итог верен, промежуточное утверждение ложно.'),
('error',False,True,True,'GCF ошибочно 11*17=187; несколько неверных факторизаций сохранены и в видимом ответе.'),
('weak',False,False,True,'Оба способа используют ранее найденный наклон 2; второй не независимый расчёт из исходных точек.'),
('error',True,True,False,'x и y независимы, но 3π/2 ошибочно отнесён к четвёртой четверти вместо границы.'),
('useful',True,False,False,'Стоимость dimes 50*10=500 и quarters 20*25=500 независимы; сумма и процент следуют после них.'),
('weak',True,False,False,'Разложения двух слагаемых независимы математически, но фраза Then, adding связывает вторую часть с первой; дальнейшие способы повторяют ответ. Консервативный отказ от тегов.'),
('weak',True,False,True,'Дробный и десятичный способы есть, но второй подан как проверка первого, итог 6 1/4 уже объявлен; Parts denominator/division зависимы.'),
('useful',True,False,False,'После общего determinant две независимые знаковые ветви: корни положительного случая и отрицательный discriminant другого.'),
('weak',False,False,True,'Цикл, его длина и счёт четвёрок зависят от одного деления 5/7.'),
('weak',False,False,True,'Второй Part лишь повторяет найденную константу -3/4.'),
('error',True,True,False,'Два уравнения независимо дают a+b=3, но написано, что a и b both equal to 3; также заявлено, что оба значения f не даны.'),
('error',True,True,False,'Пять позиционных вкладов независимы, но 12345 сначала назван четырёхзначным; далее ошибочно отрицается независимость частей.'),
('weak',False,False,True,'Построение 4x=28 и решение x=7 последовательны, второй путь повторяет их.'),
('weak',False,False,True,'Parts только задают уравнения; вычисление цены одно, затем зависимая подстановка для soda.'),
('error',True,True,True,'Появляются неверные ответы 47 и 26 при сложении промежуточных результатов; финальные Parts зависимы.'),
('error',True,True,False,'GCD/LCM вычисляются независимо, но позднее отрицается наличие 3 в 120 и выводится 200; также ложная идея оба sqrt(12000).'),
('error',True,True,False,'Неверные направления и длины 80/85.44/89.44, финальное sqrt(40²+40²)=50 ложно.'),
('error',False,True,True,'Итерации зависимы; видимые Parts 4-6 сдвинуты, шестая даёт -1/29 при итоговом 30.'),
('weak',False,False,True,'Одна линейная цепочка решения, проверка использует x=26.'),
('weak',False,False,True,'6 дней используют ранее найденные 300 worker-days; Parts последовательно зависимы.'),
('weak',True,False,False,'Сумма списка и формула независимы, но второй способ прямо ориентирован на проверку первого, а перебор содержит неясное 8: too big. Только бесспорные случаи принимаются.'),
('weak',False,False,True,'Запись уравнения и решение 6 одна цепочка; Part 1 повторяет условие.')]
assert len(items)==len(rows)==50
with (p/'screen.jsonl').open('w') as f:
 for r,(v,ind,err,dep,why) in zip(rows,items):
  f.write(json.dumps(dict(id=r['id'],verdict=v,reason=why,independent_computations_ge2=ind,false_intermediate_claims=err,dependencies_between_parts=dep),ensure_ascii=False)+'\n')
def tag(i, starts, end, outlines, conclusion):
 s=rows[i]['response']; positions=[s.index(t) for t in starts]+[s.index(end,s.index(starts[-1]))]
 goal='<Parallel><Goal>'+''.join(f'<Outline>{j+1}: {o}</Outline>' for j,o in enumerate(outlines))+'</Goal>'
 inserts={positions[0]:goal+'<Path>1: ',positions[-1]:'</Path><Conclusion>'+conclusion+'</Conclusion></Parallel>'}
 for j,pos in enumerate(positions[1:-1],2): inserts[pos]=f'</Path><Path>{j}: '
 for pos in sorted(inserts,reverse=True): s=s[:pos]+inserts[pos]+s[pos:]
 return dict(id=rows[i]['id'],question=rows[i]['question'],response=s)
accepted=[
 tag(10,['Part 1: For the 3 lions','Part 2: For the 2 rhinos'],'Total time would be',['Calculate lion recovery time.','Calculate rhino recovery time.'],'Add the two recovery times.'),
 tag(17,['For the ticket:','For the combo:'],'Adding those two',['Calculate ticket savings.','Calculate combo savings.'],'Add both savings.'),
 tag(21,['So, insulin pills:','Blood pressure pills: 3 pills/day','Anticonvulsants: 6 pills/day'],'Wait, let me check that again.',['Calculate weekly insulin pills.','Calculate weekly blood pressure pills.','Calculate weekly anticonvulsants using the common daily setup.'],'Sum the three weekly quantities.'),
 tag(25,['Let me start with the pancakes.','Next, the bacon.'],'Now, to find the total',['Calculate pancake revenue.','Calculate bacon revenue.'],'Add both revenues.'),
 tag(32,['Alright, the problem says','Then 20 quarters.'],'So total value is',['Calculate dime value in cents.','Calculate quarter value in cents.'],'Combine values and compute the quarter percentage.'),
 tag(35,['First, for Case 1:','Case 2: 2k² -7k +21 = 0\n\nDiscriminant:'],'Therefore, only k = 9/2 is valid.',['Solve the positive determinant case.','Check real roots for the negative determinant case.'],'Keep admissible positive real roots from both cases.')]
with (p/'tagged.jsonl').open('w') as f:
 for r in accepted:f.write(json.dumps(r,ensure_ascii=False)+'\n')
c=Counter(x[0] for x in items)
(p/'review.md').write_text(f'''Просмотрены все 50 полных строк input.jsonl без эталонов. Только локальное чтение и запись своей партии. Внешних вызовов и запусков нет.

Полезных и размеченных: {c['useful']}. Слабых: {c['weak']}. Ошибок: {c['error']}. Незавершённых: {c['incomplete']}.

Вердикт оценивает всё рассуждение и видимые Parts, включая позднее исправленные ошибки. useful требует двух содержательных независимых вычислений и честных границ без перестановки исходного текста. Независимость математически возможная, но не реализованная словами ответа, отдельно отражена в screen.jsonl и не гарантирует принятие.

Примеры отсева:

- gsm8k-train/3250: 120 наклеек, 12 долларов, 6 долларов. Три заголовка, одна зависимая цепочка.
- math-train/240: верный последний ответ сосуществует с GCF=187 и неверной факторизацией в Parts.
- gsm8k-train/5606: уборка и свободное время могут вычисляться независимо, но объединение задач уже стоит до второго расчёта. Переставлять текст запрещено.

В accepted сохранены исходные слова, числа и порядок. Добавлены только теги, короткие Outline и Conclusion внутри think. Первый блок math-train/7395 использует общий determinant как подготовку; знаковые случаи не читают результаты друг друга. gsm8k-train/396 использует общий расчёт 6 anticonvulsants/day до блока, три недельных расчёта независимы. Поздние проверки и повторы исходного ответа сохранены после блоков.
''')
print(dict(c), 'tagged',len(accepted))
