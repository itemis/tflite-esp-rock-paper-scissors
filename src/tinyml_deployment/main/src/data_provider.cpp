#include <iostream>
#include <array>
#include <cstdlib>
#include <cstring>
#include <iostream>

#include "data_provider.h"
#include "im_grayscale.h"

#include "app_camera_esp.h"
#include "esp_camera.h"
#include "esp_log.h"
#include "esp_spi_flash.h"
#include "esp_system.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

camera_fb_t* fb = NULL;
static const char* TAG = "app_camera";

// Get the camera module ready
TfLiteStatus InitCamera(tflite::ErrorReporter* error_reporter) {
  int ret = app_camera_init();
  if (ret != 0) {
    TF_LITE_REPORT_ERROR(error_reporter, "Camera init failed\n");
    return kTfLiteError;
  }
  TF_LITE_REPORT_ERROR(error_reporter, "Camera Initialized\n");
  return kTfLiteOk;
}

void* image_provider_get_camera_fb()
{
    return (void *)fb;
}

extern "C" int capture_image() {
  fb = esp_camera_fb_get();
  if (!fb) {
    ESP_LOGE(TAG, "Camera capture failed");
    return -1;
  }
  return 0;
}

// Begin the capture and wait for it to finish
TfLiteStatus PerformCapture(tflite::ErrorReporter* error_reporter,
                            uint8_t* image_data) {
  /* 2. Get one image with camera */
  int ret = capture_image();
  if (ret != 0) {
    return kTfLiteError;
  }
  //TF_LITE_REPORT_ERROR(error_reporter, "Image Captured"); //Image Captured
  memcpy(image_data, fb->buf, fb->len);
  esp_camera_fb_return(fb);
  /* here the esp camera can give you grayscale image directly */
  return kTfLiteOk;
}

// Get an image from the camera module
TfLiteStatus GetImage(tflite::ErrorReporter* error_reporter, int image_width,
                      int image_height, int channels, uint8_t* image_data) {
  static bool g_is_camera_initialized = false;
  if (!g_is_camera_initialized) {
    TfLiteStatus init_status = InitCamera(error_reporter);
    if (init_status != kTfLiteOk) {
      TF_LITE_REPORT_ERROR(error_reporter, "InitCamera failed\n");
      return init_status;
    }
    g_is_camera_initialized = true;
  }
  /* Camera Captures Image of size 96 x 96  which is of the format grayscale
   * thus, no need to crop or process further , directly send it to tf */
  TfLiteStatus capture_status = PerformCapture(error_reporter, image_data);
  if (capture_status != kTfLiteOk) {
    TF_LITE_REPORT_ERROR(error_reporter, "PerformCapture failed\n");
    return capture_status;
  }
  return kTfLiteOk;
}

void DataProvider::printRGBImage(std::vector<uint8_t> img, uint8_t len_x, uint8_t len_y, uint8_t len_c){
    for (int x = 0; x < len_x; ++x) {
        for (int y = 0; y < len_y; ++y) {
            for (int c = 0; c < len_c; ++c) {
                std::cout << unsigned(img[x*len_x*len_x + y*len_y + c]) << ",";
            }
            std::cout << "\n";
        }
        std::cout << "\n";
    }
    std::cout << "\n";
}

void DataProvider::printGrayImage(std::vector<uint8_t> img, uint8_t len_x, uint8_t len_y){
    for (int x = 0; x < len_x; ++x) {
        for (int y = 0; y < len_y; ++y) {
            std::cout << unsigned(img[x*len_x + y]) << ",";
        }
        std::cout << "\n";
        break;
    }
    std::cout << "\n";
}

// define periphery of MCU
// what pins receive what data and in what way
void DataProvider::dataProviderBegin(){

}

// receive sensor data
void DataProvider::gatherData(){

    // TODO: set loaded img via camera
    DataProvider::loaded_img = grayscale;

    DataProvider::printGrayImage(loaded_img, dim1, dim2);
}

// forward sensor data
std::vector<uint8_t> DataProvider::forwardData(){
    return DataProvider::loaded_img;
}

