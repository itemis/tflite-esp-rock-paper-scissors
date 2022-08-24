set(SOURCES ./src/main.cpp ./src/FeatureProvider.cpp ./src/DataProvider.cpp ./src/main_functions.cpp ./src/model_weights.cpp ./src/app_camera_esp.cpp ./src/PredictionInterpreter.cpp ./src/PredictionHandler.cpp)
idf_component_register(SRCS ${SOURCES}
                            INCLUDE_DIRS . inc
                            REQUIRES freertos esp_common tfmicro esp32-camera spi_flash)