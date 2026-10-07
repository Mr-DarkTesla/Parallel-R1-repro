# Parallel-R1: оставлен один GPU-под

2026-10-07, проверка 14:13 MSK. Две H100 освобождены: A масштабирован в 0, pod vcharkin-exp-vm-a-0 отсутствует. B vcharkin-exp-vm-b-0 Ready на ml-kub-node806.i; nvidia-smi показывает ровно две NVIDIA H100 80GB. Старый vcharkin-exp-vm остаётся в 0.

Основание: Виктор подтвердил оставить B («да делай»), затем потребовал ускорить освобождение GPU: «побыстрее уже доведи до результата и оставь только 1 под - нам надо освободить гпу». Последнее указание заменило ожидание окончания оценки A.

Оба PVC vcharkin-parallel-r1-pvc и vcharkin-parallel-r1-b-pvc сохранены, Bound. Ни один PVC или чужой ресурс не удалён. Рабочий B, его очереди и владелец 14/15 не прерывались.

Все SFT 13/14/15 завершены: 64 обновления, микробатч 2. C0 dev thinking завершился с END exit=0 в 14:06:36. Только оставшаяся 13-control-dev-think прервана; модель 7.6 GiB, полные и частичные результаты и команда очереди сохранены на исходном PVC. Три хвостовые команды сохранены для B. Перенос через ноутбук дал обрезанные архивы; частичные копии не приняты. Новому реальному Claude one_pod_recovery, PID 91220, поручены перенос через CPU без дополнительных GPU и продолжение разрешённых оценок 13/common. Matrix_continue PID 26465 продолжает 14/15.

Прежние локальные координаторы 31385, 85065, 64939 остановлены. Автоматизация parallel-r1-2-h100 остаётся PAUSED, новые расписания не созданы.

Команды операции:

```bash
kubectl --context tele.corp.mail.ru-k8s_ml_MNTINFRA_3322 -n shared-dzen-ml scale statefulset/vcharkin-exp-vm-a --replicas=0
kubectl --context tele.corp.mail.ru-k8s_ml_MNTINFRA_3322 -n shared-dzen-ml wait --for=delete pod/vcharkin-exp-vm-a-0 --timeout=40s
```

Обе команды завершились с rc=0. Независимая проверка: replicas oldmain=0/A=0/B=1, единственный оставшийся GPU-под B Ready, две физические H100, оба PVC Bound. Новых экспериментов ради освобождения ресурсов не запускали.

Локальные доказательства в /Users/v.charkin/Documents/ChatGPT/R1/outputs/reduce-to-one-pod-2026-10-07/: urgent-before-stop.json, urgent-scale-a-zero.json, urgent-wait-a-deleted.json, urgent-final-verification.json, automations-still-off.json. Рядом outputs/instruct4b-2026-10-06/GPU_RELEASED.json и one_pod_recovery/task.md.

GPU_RELEASED подтверждает освобождение ресурсов. SINGLE_POD_READY пока отсутствует: он допустим после переноса модели 13 и передачи оценок. Не считать незавершённые оценки готовыми; не поднимать A для повтора.
