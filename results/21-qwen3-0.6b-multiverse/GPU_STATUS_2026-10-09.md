# GPU и монтирование собственного pod B, 9 октября 2026

Кластерный контекст: `tele.corp.mail.ru-k8s_ml_MNTINFRA_3322`, namespace `shared-dzen-ml`. Проверялись только собственные ресурсы `vcharkin-*`; чужие поды, профили и PVC не изменялись.

Перед запуском не было процесса `exp21_06b` с прежним PID 88500. Собственный StatefulSet `vcharkin-exp-vm-b` был масштабирован с 0 до 1. Он запрашивает одну H100 PA и монтирует только собственный PVC `vcharkin-parallel-r1-b-pvc` в `/work`. Под `vcharkin-exp-vm-b-0` был назначен планировщиком на `ml-kub-node801.i`; событие `SuccessfulAttachVolume` подтвердило attach `pvc-6ff59ce0-7936-4aa0-a131-481e19aa4de3`. Контейнер остался в `ContainerCreating`; kubelet повторял:

```text
Warning FailedMount Unable to attach or mount volumes: unmounted volumes=[work],
unattached volumes=[dshm work kube-api-access-c8x7z gitconfig user-vault-token]:
timed out waiting for the condition
```

Через примерно 11 минут B возвращён к 0, чтобы не удерживать GPU без работающего контейнера. Контейнер не стартовал, команды обучения на GPU не запускались. Проверка после остановки: A и B оба `replicas=0`, pod B отсутствует, B PVC `Bound` (200Gi); PVC не удаляли. Последующие события pod уже исчезли из короткого списка Kubernetes, поэтому сохранён точный текст из диагностики во время сбоя.

У пользователя нет права читать cluster-scoped `volumeattachments.storage.k8s.io`: `Forbidden` для `v.charkin`. Поэтому по доступным данным нельзя назвать корневую причину `NodeStageVolume`/`NodePublishVolume`. У pod A отдельный собственный `vcharkin-parallel-r1-pvc` (200Gi, Bound), а текущая конфигурация A запрашивает одну H100 PA; запуск A после 09:00 отдельно уточнён у пользователя. До ответа A остаётся выключен. Старые StatefulSet и PVC не трогали.

## Готовый текст коллегам или поддержке кластера

> Привет! В `shared-dzen-ml` мой pod `vcharkin-exp-vm-b-0` с одной H100 был назначен на `ml-kub-node801.i`, но примерно 11 минут оставался в `ContainerCreating`. Для моего PVC `vcharkin-parallel-r1-b-pvc` (PV `pvc-6ff59ce0-7936-4aa0-a131-481e19aa4de3`) было событие `SuccessfulAttachVolume`, затем повторялся `FailedMount` тома `work`: `timed out waiting for the condition`. Я вернул StatefulSet к 0; PVC остался `Bound`, GPU освобождена. Можете посмотреть причину в логах kubelet/CSI `NodeStageVolume` или `NodePublishVolume` на node801 и подсказать безопасный способ восстановить монтирование? PVC, пожалуйста, не удаляйте. У меня нет RBAC на `VolumeAttachment`, поэтому глубже диагностировать attach не могу.
