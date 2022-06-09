/* Copyright 2019 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#include "main_functions.h"
#include "esp_log.h"
#include "esp_system.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

void tf_main(int argc, char* argv[]) {
  setup();
  while (true) {
    loop();
  }
}

extern void task_initI2C(void*);

extern "C" void app_main() {
  //xTaskCreate(&task_initI2C, "mpu_task", 2048, NULL, 5, NULL);
  //vTaskDelay(500/portTICK_PERIOD_MS);

  // https://www.freertos.org/a00125.html
  // https://www.freertos.org/FAQMem.html#StackSize
  // TODO: we have chosen the value 10*1024 based on tutorials; value not optimized
  xTaskCreate((TaskFunction_t)&tf_main, "tensorflow", 20 * 1024, NULL, 8, NULL);
  vTaskDelete(NULL);
}