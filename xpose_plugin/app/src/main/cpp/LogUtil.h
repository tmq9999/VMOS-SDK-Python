#ifndef VMOS_LOGUTIL_H
#define VMOS_LOGUTIL_H

#include <android/log.h>

#define LOG_TAG "VMOSNative"
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO,  LOG_TAG, __VA_ARGS__)
#define LOGE(...) __android_log_print(ANDROID_LOG_ERROR, LOG_TAG, __VA_ARGS__)
#define LOGD(...) __android_log_print(ANDROID_LOG_DEBUG, LOG_TAG, __VA_ARGS__)

#endif /* VMOS_LOGUTIL_H */
