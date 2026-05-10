<template>
  <div
    class="upload-zone"
    :class="{ dragover: isDragover }"
    @dragover.prevent="isDragover = true"
    @dragleave="isDragover = false"
    @drop.prevent="handleDrop"
    @click="triggerInput"
  >
    <input
      ref="fileInput"
      type="file"
      accept=".pdf,.md,.txt,.docx"
      multiple
      @change="handleFileSelect"
      hidden
    />
    <div class="upload-icon">+</div>
    <div class="upload-text">
      拖拽教材文件到此处<br>
      或点击选择文件
    </div>
    <div class="upload-hint">支持 PDF、Markdown、TXT、DOCX</div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { uploadTextbook } from '../api'

export default {
  name: 'UploadZone',
  emits: ['uploaded', 'error'],
  setup(props, { emit }) {
    const fileInput = ref(null)
    const isDragover = ref(false)

    // 触发文件选择
    const triggerInput = () => fileInput.value?.click()

    // 处理文件选择
    const handleFileSelect = async (e) => {
      const files = e.target.files
      await uploadFiles(files)
      fileInput.value.value = ''  // 清空以便重复选择同一文件
    }

    // 处理拖拽
    const handleDrop = async (e) => {
      isDragover.value = false
      const files = e.dataTransfer.files
      await uploadFiles(files)
    }

    // 上传文件
    const uploadFiles = async (files) => {
      for (const file of files) {
        try {
          await uploadTextbook(file)
          emit('uploaded', file.name)
        } catch (err) {
          emit('error', { file: file.name, error: err })
        }
      }
    }

    return { fileInput, isDragover, triggerInput, handleFileSelect, handleDrop }
  }
}
</script>

<style scoped>
.upload-zone {
  margin: 16px;
  padding: 32px 16px;
  border: 2px dashed #ddd;
  border-radius: 8px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.upload-zone:hover,
.upload-zone.dragover {
  border-color: #1890ff;
  background: #f0f7ff;
}

.upload-icon {
  font-size: 48px;
  color: #ccc;
  margin-bottom: 8px;
}

.upload-text {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
}

.upload-hint {
  margin-top: 8px;
  color: #999;
  font-size: 12px;
}
</style>