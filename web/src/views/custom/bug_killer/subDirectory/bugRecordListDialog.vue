<template>
  <el-drawer
    title="操作记录"
    :visible.sync="visible"
    direction="rtl"
    size="50%"
    @close="handleClose">
    <template slot="title">
      <h3>当前bug名称：{{ bugObj ? bugObj.title : '无' }}</h3>
    </template>
    <div style="padding: 20px 40px">
      <el-timeline :reverse=true>
        <el-timeline-item
          v-for="(record, index) in recordList"
          :key="index"
          :timestamp="record.create_datetime">
          {{ record.content }}
          <el-tag size="small">{{ record.creator_name }}</el-tag>
        </el-timeline-item>
      </el-timeline>
    </div>
  </el-drawer>

</template>

<script>
import {GetBugRecordList} from "@/views/custom/bug_killer/subDirectory/api";

export default {
  name: "bugRecordList",
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    bugObj: {
      type: Object,
      default: () => {}
    },
    recordList: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {}
  },
  methods: {
    fetchRecordList() {
      let query = {
        bug: this.bugObj.id,
        status: 1,
        limit: 999
      }
      GetBugRecordList(query).then(ret => {
        this.recordList = ret.data.data
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
