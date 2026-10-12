# exps/branch-review-20261007

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Метрики и полнота результатов

- [exps/branch-review-20261007/latest-s2.json](../artifacts/exps/branch-review-20261007/latest-s2.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "observed_at": "2026-10-07T16:28:53.745304+00:00",
  "status": {
    "state": "complete",
    "observed_utc": "2026-10-07T15:43:24.000523+00:00",
    "exit_code": 0
  },
  "alive": false,
  "age_s": 2731.779446363449,
  "metrics": "470 records; see original artifact"
}
```

</details>

- [exps/branch-review-20261007/live-metrics.json](../artifacts/exps/branch-review-20261007/live-metrics.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "observed_at": "2026-10-07T15:02:07.043431+00:00",
  "runs": {
    "rl-unseen-s1-20261006": {
      "files": {
        "status.json": {
          "state": "stopped-for-resume",
          "checkpoint": "${PROJECT_ROOT}/exps/rl-unseen-s1-20261006/results/checkpoints/global_step_60",
          "next_run": "${PROJECT_ROOT}/exps/rl-unseen-s1-20261007-seq128",
          "at": 1791326053.9068418
        }
      },
      "logs": {
        "driver.log": {
          "mtime": 1791326039.4090748,
          "age_s": 59287.65650701523,
          "metrics": "60 records; see original artifact",
          "errors": [
            "\u001b[36m(TaskRunner pid=511885)\u001b[0m Traceback (most recent call last):"
          ]
        }
      },
      "validation_files": [
        {
          "step": "0",
          "bytes": 59898555,
          "mtime": 1791315800.4338782,
          "rows": 1916
        },
        {
          "step": "10",
          "bytes": 60526276,
          "mtime": 1791317821.3287578,
          "rows": 1916
        },
        {
          "step": "20",
          "bytes": 59927275,
          "mtime": 1791319682.9355934,
          "rows": 1916
        },
        {
          "step": "30",
          "bytes": 59933738,
          "mtime": 1791321529.7655356,
          "rows": 1916
        },
        {
          "step": "40",
          "bytes": 59674581,
          "mtime": 1791323302.4533744,
          "rows": 1916
        },
        {
          "step": "50",
          "bytes": 60658740,
          "mtime": 1791324703.2131853,
          "rows": 1916
        },
        {
          "step": "60",
          "bytes": 60602727,
          "mtime": 1791326007.4780436,
          "rows": 1916
        }
      ]
    },
    "rl-unseen-s1-20261007-seq128": {
      "files": {
        "status.json": {
          "state": "stopped-for-s2",
          "checkpoint": "${PROJECT_ROOT}/exps/rl-unseen-s1-20261007-seq128/results/checkpoints/global_step_280",
          "verified_hf": "${PROJECT_ROOT}/exps/rl-unseen-s1-20261007-seq128/exports/hf-step280",
          "next_run": "${PROJECT_ROOT}/exps/rl-unseen-s2-20261007",
          "at": 1791356001.378862
        },
        "export-step300.json": {
          "state": "cancelled",
          "reason": "User selected independent S2; S1 stopped at durable280 with verified HF",
          "at": 1791356001.3768938
        }
      },
      "logs": {
        "driver.log": {
          "mtime": 1791355969.9997773,
          "age_s": 29357.7304315567,
          "metrics": "220 records; see original artifact",
          "errors": [
            "\u001b[36m(TaskRunner pid=538993)\u001b[0m Traceback (most recent call last):"
          ]
        }
      },
      "validation_files": [
        {
          "step": "100",
          "bytes": 59428633,
          "mtime": 1791332003.8848455,
          "rows": 1916
        },
        {
          "step": "110",
          "bytes": 59462312,
          "mtime": 1791333298.0577242,
          "rows": 1916
        },
        {
          "step": "120",
          "bytes": 58679830,
          "mtime": 1791334580.417467,
          "rows": 1916
        },
        {
          "step": "130",
          "bytes": 58489075,
          "mtime": 1791335866.1563826,
          "rows": 1916
        },
        {
          "step": "140",
          "bytes": 58306449,
          "mtime": 1791337151.055279,
          "rows": 1916
        },
        {
          "step": "150",
          "bytes": 59030349,
          "mtime": 1791338426.1932254,
          "rows": 1916
        },
        {
          "step": "160",
          "bytes": 57889999,
          "mtime": 1791339706.8822641,
          "rows": 1916
        },
        {
          "step": "170",
          "bytes": 56742246,
          "mtime": 1791341061.6900477,
          "rows": 1916
        },
        {
          "step": "180",
          "bytes": 56875293,
          "mtime": 1791342419.8360412,
          "rows": 1916
        },
        {
          "step": "190",
          "bytes": 57614264,
          "mtime": 1791343762.265036,
          "rows": 1916
        },
        {
          "step": "200",
          "bytes": 57579799,
          "mtime": 1791345092.5379386,
          "rows": 1916
        },
        {
          "step": "210",
          "bytes": 56509724,
          "mtime": 1791346467.0467002,
          "rows": 1916
        },
        {
          "step": "220",
          "bytes": 57510287,
          "mtime": 1791347781.341611,
          "rows": 1916
        },
        {
          "step": "230",
          "bytes": 57687146,
          "mtime": 1791349098.7364416,
          "rows": 1916
        },
        {
          "step": "240",
          "bytes": 57063134,
          "mtime": 1791350433.147522,
          "rows": 1916
        },
        {
          "step": "250",
          "bytes": 56625486,
          "mtime": 1791351789.9772987,
          "rows": 1916
        },
        {
          "step": "260",
          "bytes": 57034107,
          "mtime": 1791353173.279258,
          "rows": 1916
        },
        {
          "step": "270",
          "bytes": 58023143,
          "mtime": 1791354534.0481498,
          "rows": 1916
        },
        {
          "step": "280",
          "bytes": 58375525,
          "mtime": 1791355881.9091535,
          "rows": 1916
        },
        {
          "step": "70",
          "bytes": 60844795,
          "mtime": 1791327994.1169972,
          "rows": 1916
        },
        {
          "step": "80",
          "bytes": 60208350,
          "mtime": 1791329438.898996,
          "rows": 1916
        },
        {
          "step": "90",
          "bytes": 60590709,
          "mtime": 1791330739.2647843,
          "rows": 1916
        }
      ]
    },
    "rl-unseen-s1-bs32-20261007": {
      "files": {
        "status.json": {
          "state": "complete",
          "observed_utc": "2026-10-07T11:12:28.866241+00:00",
          "exit_code": 0
        },
        "launched.json": {
          "at": 1791360061.9201498
        },
        "export-step300.json": {
          "state": "complete",
          "at": 1791371461.1032193,
          "step": 300,
          "source": "${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/results/checkpoints/global_step_300",
          "target": "${PROJECT_ROOT}/exps/rl-unseen-s1-bs32-20261007/exports/hf-step300",
          "bytes": 1518118104
        }
      },
      "logs": {
        "driver.log": {
          "mtime": 1791371544.9442022,
          "age_s": 13785.123875617981,
          "metrics": "210 records; see original artifact",
          "errors": [
            "\u001b[36m(TaskRunner pid=648296)\u001b[0m Traceback (most recent call last):",
            "\u001b[36m(TaskRunner pid=648296)\u001b[0m Traceback (most recent call last):"
          ]
        },
        "validation-every10/driver.log": {
          "mtime": 1791364520.158476,
          "age_s": 20809.925580501556,
          "metrics": "90 records; see original artifact",
          "errors": [
            "\u001b[36m(TaskRunner pid=624285)\u001b[0m Traceback (most recent call last):"
          ]
        }
      },
      "validation_files": [
        {
          "step": "10",
          "bytes": 60037008,
          "mtime": 1791361137.1635456,
          "rows": 1916
        },
        {
          "step": "100",
          "bytes": 60927535,
          "mtime": 1791365360.5581691,
          "rows": 1916
        },
        {
          "step": "150",
          "bytes": 60984817,
          "mtime": 1791366907.378092,
          "rows": 1916
        },
        {
          "step": "20",
          "bytes": 59594387,
          "mtime": 1791361655.415364,
          "rows": 1916
        },
        {
          "step": "200",
          "bytes": 60598436,
          "mtime": 1791368375.3410923,
          "rows": 1916
        },
        {
          "step": "250",
          "bytes": 61141088,
          "mtime": 1791369846.11686,
          "rows": 1916
        },
        {
          "step": "30",
          "bytes": 58816848,
          "mtime": 1791362054.017619,
          "rows": 1916
        },
        {
          "step": "300",
          "bytes": 54464398,
          "mtime": 1791371492.3887033,
          "rows": 1916
        },
        {
          "step": "40",
          "bytes": 58474820,
          "mtime": 1791362471.0265684,
          "rows": 1916
        },
        {
          "step": "50",
          "bytes": 58457520,
          "mtime": 1791362877.5354466,
          "rows": 1916
        },
        {
          "step": "60",
          "bytes": 58926688,
          "mtime": 1791363281.3993163,
          "rows": 1916
        },
        {
          "step": "70",
          "bytes": 59031748,
          "mtime": 1791363689.2882652,
          "rows": 1916
        },
        {
          "step": "80",
          "bytes": 59130184,
          "mtime": 1791364084.0512187,
          "rows": 1916
        },
        {
          "step": "90",
          "bytes": 60163239,
          "mtime": 1791364468.1102014,
          "rows": 1916
        }
      ]
    },
    "rl-unseen-s2-20261007": {
      "files": {
        "status.json": {
          "state": "paused_user_requested_s1_bs32",
          "at": 1791359977.780969,
          "checkpoint": "${PROJECT_ROOT}/exps/rl-unseen-s2-20261007/results/checkpoints/global_step_20",
          "completed_steps": 20
        },
        "export-step300.json": {
          "state": "cancelled_user_switch",
          "at": 1791359977.7828577
        }
      },
      "logs": {
        "driver.log": {
          "mtime": 1791359819.6317909,
          "age_s": 25511.851018428802,
          "metrics": [],
          "errors": []
        }
      },
      "validation_files": [
        {
          "step": "10",
          "bytes": 60677697,
          "mtime": 1791358349.324886,
          "rows": 1916
        },
        {
          "step": "20",
          "bytes": 61149812,
          "mtime": 1791359537.827763,
          "rows": 1916
        }
      ]
    },
    "rl-unseen-s2-bs32-20261007": {
      "files": {
        "status.json": {
          "state": "paused_user_requested",
          "observed_utc": "2026-10-07T11:43:23.812098+00:00",
          "last_logged_step": 33,
          "last_checkpoint": 30,
          "checkpoint_complete": true,
          "checkpoint_files": 25,
          "owned_processes_remaining": [],
          "gpu_processes_remaining": [],
          "resume_requires_user_request": true,
          "stopped_controller_pid": 667589,
          "stopped_export300_pid": 667590
        },
        "launched.json": {
          "at": 1791371803.5335557,
          "export300_pid": 667590,
          "origin": "original Unseen-SFT",
          "batch": 32,
          "stage": "s2",
          "steps": 300,
          "gpus": [
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7
          ]
        },
        "user-stop.json": {
          "state": "paused_user_requested",
          "observed_utc": "2026-10-07T11:43:23.812098+00:00",
          "last_logged_step": 33,
          "last_checkpoint": 30,
          "checkpoint_complete": true,
          "checkpoint_files": 25,
          "owned_processes_remaining": [],
          "gpu_processes_remaining": [],
          "resume_requires_user_request": true,
          "stopped_controller_pid": 667589,
          "stopped_export300_pid": 667590
        },
        "export-step300.json": {
          "state": "cancelled_user_requested",
          "at": 1791373403.81648,
          "step": 300,
          "source": "${PROJECT_ROOT}/exps/rl-unseen-s2-bs32-20261007/results/checkpoints/global_step_300",
          "target": "${PROJECT_ROOT}/exps/rl-unseen-s2-bs32-20261007/exports/hf-step300"
        }
      },
      "logs": {
        "driver.log": {
          "mtime": 1791373323.7320418,
          "age_s": 12007.93364238739,
          "metrics": [
            {
              "parallel/ratio": 0.92578125,
              "training/global_step": 1.0,
              "critic/score/mean": -0.9609375,
              "response_length/mean": 1056.375,
              "timing_s/step": 123.48003195691854
            },
            {
              "parallel/ratio": 0.9296875,
              "training/global_step": 2.0,
              "critic/score/mean": -0.9296875,
              "response_length/mean": 1050.1796875,
              "timing_s/step": 34.81593233346939
            },
            {
              "parallel/ratio": 0.93359375,
              "training/global_step": 3.0,
              "critic/score/mean": -0.890625,
              "response_length/mean": 911.6484375,
              "timing_s/step": 34.124740563333035
            },
            {
              "parallel/ratio": 0.93359375,
              "training/global_step": 4.0,
              "critic/score/mean": -0.8515625,
              "response_length/mean": 901.15625,
              "timing_s/step": 34.55474669858813
            },
            {
              "parallel/ratio": 0.9140625,
              "training/global_step": 5.0,
              "critic/score/mean": -0.96875,
              "response_length/mean": 990.0546875,
              "timing_s/step": 34.478114132769406
            },
            {
              "parallel/ratio": 0.94140625,
              "training/global_step": 6.0,
              "critic/score/mean": -0.8515625,
              "response_length/mean": 960.89453125,
              "timing_s/step": 28.890892856754363
            },
            {
              "parallel/ratio": 0.94921875,
              "training/global_step": 7.0,
              "critic/score/mean": -0.859375,
              "response_length/mean": 1039.13671875,
              "timing_s/step": 32.08687339257449
            },
            {
              "parallel/ratio": 0.93359375,
              "training/global_step": 8.0,
              "critic/score/mean": -0.90625,
              "response_length/mean": 988.5703125,
              "timing_s/step": 31.847809806466103
            },
            {
              "parallel/ratio": 0.8984375,
              "training/global_step": 9.0,
              "critic/score/mean": -0.9070312976837158,
              "response_length/mean": 1062.36328125,
              "timing_s/step": 33.766484023071826
            },
            {
              "parallel/ratio": 0.88671875,
              "training/global_step": 10.0,
              "critic/score/mean": -0.871874988079071,
              "response_length/mean": 931.9375,
              "timing_s/save_checkpoint": 37.273166990838945,
              "timing_s/step": 69.02904157992452
            },
            {
              "parallel/ratio": 0.93359375,
              "training/global_step": 11.0,
              "critic/score/mean": -0.9375,
              "response_length/mean": 1063.8984375,
              "timing_s/step": 35.57622503954917
            },
            {
              "parallel/ratio": 0.9140625,
              "training/global_step": 12.0,
              "critic/score/mean": -0.9296875,
              "response_length/mean": 1120.23828125,
              "timing_s/step": 33.45242125540972
            },
            {
              "parallel/ratio": 0.890625,
              "training/global_step": 13.0,
              "critic/score/mean": -0.90625,
              "response_length/mean": 933.79296875,
              "timing_s/step": 30.76131090708077
            },
            {
              "parallel/ratio": 0.88671875,
              "training/global_step": 14.0,
              "critic/score/mean": -0.8984375,
              "response_length/mean": 1030.13671875,
              "timing_s/step": 32.66851605847478
            },
            {
              "parallel/ratio": 0.91796875,
              "training/global_step": 15.0,
              "critic/score/mean": -0.921875,
              "response_length/mean": 1021.0078125,
              "timing_s/step": 30.075757601298392
            },
            {
              "parallel/ratio": 0.890625,
              "training/global_step": 16.0,
              "critic/score/mean": -0.921875,
              "response_length/mean": 919.07421875,
              "timing_s/step": 29.311522335745394
            },
            {
              "parallel/ratio": 0.8984375,
              "training/global_step": 17.0,
              "critic/score/mean": -0.90625,
              "response_length/mean": 988.37890625,
              "timing_s/step": 28.590240661986172
            },
            {
              "parallel/ratio": 0.87890625,
              "training/global_step": 18.0,
              "critic/score/mean": -0.9296875,
              "response_length/mean": 911.828125,
              "timing_s/step": 28.62252845801413
            },
            {
              "parallel/ratio": 0.8984375,
              "training/global_step": 19.0,
              "critic/score/mean": -0.8890625238418579,
              "response_length/mean": 892.359375,
              "timing_s/step": 29.747842280194163
            },
            {
              "parallel/ratio": 0.8671875,
              "training/global_step": 20.0,
              "critic/score/mean": -0.9250000715255737,
              "response_length/mean": 916.7421875,
              "timing_s/save_checkpoint": 42.70536473672837,
              "timing_s/step": 68.37695890385658
            },
            {
              "parallel/ratio": 0.90234375,
              "training/global_step": 21.0,
              "critic/score/mean": -0.859375,
              "response_length/mean": 897.953125,
              "timing_s/step": 27.359983471222222
            },
            {
              "parallel/ratio": 0.875,
              "training/global_step": 22.0,
              "critic/score/mean": -0.984375,
              "response_length/mean": 880.53515625,
              "timing_s/step": 26.36454660166055
            },
            {
              "parallel/ratio": 0.89453125,
              "training/global_step": 23.0,
              "critic/score/mean": -0.9609375,
              "response_length/mean": 913.46875,
              "timing_s/step": 27.731494698673487
            },
            {
              "parallel/ratio": 0.88671875,
              "training/global_step": 24.0,
              "critic/score/mean": -0.9453125,
              "response_length/mean": 1061.30859375,
              "timing_s/step": 34.80499478429556
            },
            {
              "parallel/ratio": 0.84765625,
              "training/global_step": 25.0,
              "critic/score/mean": -0.8828125,
              "response_length/mean": 959.7734375,
              "timing_s/step": 24.79164402652532
            },
            {
              "parallel/ratio": 0.8828125,
              "training/global_step": 26.0,
              "critic/score/mean": -0.9296875,
              "response_length/mean": 1004.14453125,
              "timing_s/step": 33.80761285405606
            },
            {
              "parallel/ratio": 0.875,
              "training/global_step": 27.0,
              "critic/score/mean": -0.9140625,
              "response_length/mean": 968.328125,
              "timing_s/step": 33.837787913158536
            },
            {
              "parallel/ratio": 0.875,
              "training/global_step": 28.0,
              "critic/score/mean": -0.953125,
              "response_length/mean": 993.48046875,
              "timing_s/step": 28.687873367220163
            },
            {
              "parallel/ratio": 0.875,
              "training/global_step": 29.0,
              "critic/score/mean": -0.907031238079071,
              "response_length/mean": 1054.77734375,
              "timing_s/step": 33.79835111834109
            },
            {
              "parallel/ratio": 0.87890625,
              "training/global_step": 30.0,
              "critic/score/mean": -0.9320312738418579,
              "response_length/mean": 897.16796875,
              "timing_s/save_checkpoint": 39.566228499636054,
              "timing_s/step": 67.33233232051134
            },
            {
              "parallel/ratio": 0.87890625,
              "training/global_step": 31.0,
              "critic/score/mean": -0.8984375,
              "response_length/mean": 891.83203125,
              "timing_s/step": 26.66631123237312
            },
            {
              "parallel/ratio": 0.84765625,
              "training/global_step": 32.0,
              "critic/score/mean": -0.8359375,
              "response_length/mean": 1039.14453125,
              "timing_s/step": 29.446683985181153
            },
            {
              "parallel/ratio": 0.8671875,
              "training/global_step": 33.0,
              "critic/score/mean": -0.9296875,
              "response_length/mean": 862.1484375,
              "timing_s/step": 26.527748813852668
            }
          ],
          "errors": []
        }
      },
      "validation_files": []
    },
    "rl-unseen-s2-bs32-500-20261007": {
      "files": {
        "status.json": {
          "state": "running",
          "observed_utc": "2026-10-07T12:40:37.604280+00:00",
          "steps": 500,
          "resume_checkpoint": "${PROJECT_ROOT}/exps/rl-unseen-s2-bs32-20261007/results/checkpoints/global_step_30",
          "gpus": [
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7
          ]
        },
        "weights-only-check.json": {
          "verified": true,
          "step": 30,
          "finite_weights": true,
          "cpu_forward_finite": true,
          "no_training_state": true,
          "control_token_ids": [
            [
              151671
            ],
            [
              151672
            ],
            [
              151669
            ],
            [
              151670
            ],
            [
              151673
            ],
            [
              151674
            ]
          ],
          "bytes": 3020313168
        }
      },
      "logs": {
        "driver.log": {
          "mtime": 1791385331.665982,
          "age_s": 0.04853677749633789,
          "metrics": "369 records; see original artifact",
          "errors": [
            "\u001b[36m(TaskRunner pid=699674)\u001b[0m Traceback (most recent call last):"
          ]
        }
      },
      "validation_files": [
        {
          "step": "100",
          "bytes": 62129139,
          "mtime": 1791379232.2002034,
          "rows": 1916
        },
        {
          "step": "150",
          "bytes": 65207151,
          "mtime": 1791380376.8441868,
          "rows": 1916
        },
        {
          "step": "200",
          "bytes": 67421633,
          "mtime": 1791381319.8021011,
          "rows": 1916
        },
        {
          "step": "250",
          "bytes": 67984243,
          "mtime": 1791382200.0111547,
          "rows": 1916
        },
        {
          "step": "300",
          "bytes": 66579304,
          "mtime": 1791383181.9150684,
          "rows": 1916
        },
        {
          "step": "350",
          "bytes": 67094511,
          "mtime": 1791384183.0509863,
          "rows": 1916
        },
        {
          "step": "400",
          "bytes": 64416097,
          "mtime": 1791385292.7209558,
          "rows": 1916
        },
        {
          "step": "50",
          "bytes": 61370724,
          "mtime": 1791377865.4392672,
          "rows": 1916
        }
      ],
      "pid_alive": true,
      "controller_pid_alive": true
    }
  }
}
```

</details>

- [exps/branch-review-20261007/response-length-summary.json](../artifacts/exps/branch-review-20261007/response-length-summary.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "S1 · batch 256": {
    "first50_mean": 971.95958984375,
    "last50_mean": 1109.789755859375,
    "last10_mean": 1074.587158203125,
    "windows": [
      {
        "start": 1,
        "end": 50,
        "logged_steps": 50,
        "mean_tokens": 971.95958984375
      },
      {
        "start": 51,
        "end": 100,
        "logged_steps": 49,
        "mean_tokens": 943.8129085618623
      },
      {
        "start": 101,
        "end": 150,
        "logged_steps": 50,
        "mean_tokens": 1010.84974609375
      },
      {
        "start": 151,
        "end": 200,
        "logged_steps": 50,
        "mean_tokens": 1091.94775390625
      },
      {
        "start": 201,
        "end": 250,
        "logged_steps": 50,
        "mean_tokens": 1112.433564453125
      },
      {
        "start": 251,
        "end": 280,
        "logged_steps": 30,
        "mean_tokens": 1101.7155436197916
      }
    ]
  },
  "S1 · batch 32": {
    "first50_mean": 1020.513125,
    "last50_mean": 1050.568046875,
    "last10_mean": 1210.739453125,
    "windows": [
      {
        "start": 1,
        "end": 50,
        "logged_steps": 50,
        "mean_tokens": 1020.513125
      },
      {
        "start": 51,
        "end": 100,
        "logged_steps": 50,
        "mean_tokens": 1005.22921875
      },
      {
        "start": 101,
        "end": 150,
        "logged_steps": 50,
        "mean_tokens": 926.150546875
      },
      {
        "start": 151,
        "end": 200,
        "logged_steps": 50,
        "mean_tokens": 962.315546875
      },
      {
        "start": 201,
        "end": 250,
        "logged_steps": 50,
        "mean_tokens": 935.998046875
      },
      {
        "start": 251,
        "end": 300,
        "logged_steps": 50,
        "mean_tokens": 1050.568046875
      }
    ]
  },
  "S2 · batch 32": {
    "first50_mean": 966.4946875,
    "last50_mean": 825.325546875,
    "last10_mean": 906.713671875,
    "windows": [
      {
        "start": 1,
        "end": 50,
        "logged_steps": 50,
        "mean_tokens": 966.4946875
      },
      {
        "start": 51,
        "end": 100,
        "logged_steps": 50,
        "mean_tokens": 871.9721875
      },
      {
        "start": 101,
        "end": 150,
        "logged_steps": 50,
        "mean_tokens": 808.45625
      },
      {
        "start": 151,
        "end": 200,
        "logged_steps": 50,
        "mean_tokens": 605.7321875
      },
      {
        "start": 201,
        "end": 250,
        "logged_steps": 50,
        "mean_tokens": 514.043359375
      },
      {
        "start": 251,
        "end": 300,
        "logged_steps": 50,
        "mean_tokens": 561.413359375
      },
      {
        "start": 301,
        "end": 350,
        "logged_steps": 50,
        "mean_tokens": 546.42921875
      },
      {
        "start": 351,
        "end": 400,
        "logged_steps": 50,
        "mean_tokens": 622.54421875
      },
      {
        "start": 401,
        "end": 450,
        "logged_steps": 50,
        "mean_tokens": 749.9021875
      },
      {
        "start": 451,
        "end": 500,
        "logged_steps": 50,
        "mean_tokens": 825.325546875
      }
    ]
  }
}
```

</details>

- [exps/branch-review-20261007/summary.json](../artifacts/exps/branch-review-20261007/summary.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "observed_at": "2026-10-07T16:28:53.745304+00:00",
  "s2_last_step": 500,
  "s2_alive": false,
  "s2_log_age_s": 2731.779446363449,
  "baseline_math": 0.25949367088607594,
  "S1 · batch 256 · остановлен на 280": {
    "latest_validation_step": 280,
    "math": 0.4936708860759494
  },
  "S1 · batch 32 · завершён, 300 шагов": {
    "latest_validation_step": 300,
    "math": 0.3670886075949367
  },
  "S2 · batch 32 · 500/500, завершён": {
    "latest_validation_step": 500,
    "math": 0.3860759493670886
  },
  "s2_parallel_last10": 0.000390625
}
```

</details>

## Графики

- [exps/branch-review-20261007/response-length.png](../artifacts/exps/branch-review-20261007/response-length.png) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/branch-review-20261007/response-length.svg](../artifacts/exps/branch-review-20261007/response-length.svg) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/branch-review-20261007/rl-progress.png](../artifacts/exps/branch-review-20261007/rl-progress.png) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/branch-review-20261007/rl-progress.svg](../artifacts/exps/branch-review-20261007/rl-progress.svg) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

## Исходники рецепта и награды

- [exps/branch-review-20261007/plot.py](../artifacts/exps/branch-review-20261007/plot.py) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

- [exps/branch-review-20261007/plot_lengths.py](../artifacts/exps/branch-review-20261007/plot_lengths.py) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.
