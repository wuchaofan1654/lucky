<template>
  <el-dialog
    title="解决问题"
    :visible.sync="visible"
    width="40%"
    @close="handleClose"
    center>
    <el-form :model="bugObj" label-width="120px">
      <el-form-item label="问题原因">
        <el-select v-model="bugObj.cause_reason">
          <el-option v-for="item in causeReasonOptions" :label="item.label" :value="item.value"/>
        </el-select>
      </el-form-item>
      <el-form-item label="解决方案">
        <el-select v-model="bugObj.solution">
          <el-option v-for="item in solutionOptions" :label="item.label" :value="item.value"/>
        </el-select>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button @click="visible=false">取 消</el-button>
      <el-button type="primary" @click="submit">确 定</el-button>
    </span>
  </el-dialog>
</template>

<script>

import {UpdateBug} from '../api'

export default {
  name: "closeBugDialog",
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    bugObj: {
      type: Object,
      default: () => {}
    },
    solutionOptions: {
      type: Array,
      default: () => []
    },
    causeReasonOptions: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    submit() {
      this.visible = false
      this.bugObj.status = 2
      if (this.bugObj instanceof Array) {
        this.bugObj.resource = this.bugObj.resource.join(',')
      }
      UpdateBug(this.bugObj).then(ret=>{
        this.$message.success(ret.msg)
      })
    },
    handleClose() {
      this.$emit('changeVisible')
    }
  }
}
</script>

<style scoped>

</style>
