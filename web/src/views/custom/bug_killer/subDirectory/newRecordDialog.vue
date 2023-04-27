<template>
  <el-dialog
    title="添加备注"
    :visible.sync="visible"
    width="40%"
    @close="handleClose"
    center>
    <el-input type="textarea" :rows="10" v-model="text" placeholder="请选择" />
    <span slot="footer" class="dialog-footer">
      <el-button @click="visible=false">取 消</el-button>
      <el-button type="primary" @click="submit">确 定</el-button>
    </span>
  </el-dialog>
</template>

<script>
import {AddBugRecord} from "@/views/custom/bug_killer/subDirectory/api";

export default {
  name: "newRecordListDialog",
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    bugObj: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      text: ''
    }
  },
  methods: {
    submit() {
      let query = {
        bug: this.bugObj.id,
        content: this.text,
      }
      AddBugRecord(query).then(ret=>{
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
