<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @fetchRecords="onFetchRecordList"
      @addNewRecord="onAddNewRecord"
      @closeBug="onCloseBug"
      @solveBug="onSolveBug">
      <el-button size="small" type="primary" @click="lineEditAdd()"><i class="el-icon-plus"/> 新增</el-button>
      <div slot="header">
        <crud-search
          ref="search"
          :options="crud.searchOptions"
          @submit="handleSearch"
        />
        <el-button-group>
          <el-button
            size="small"
            type="danger"
            @click="batchDelete"
          ><i class="el-icon-delete"/> 批量删除
          </el-button>
          <el-button
            size="small"
            type="primary"
            @click="addRow"
            v-permission="'Create'"
          ><i class="el-icon-plus"/> 新建
          </el-button>
          <el-button
            size="small"
            type="warning"
            @click="onExport"
            v-permission="'Export'"
          ><i class="el-icon-download"/> 导出
          </el-button>
          <importExcel
            api="api/custom/bug/"
            v-permission="'Import'"
            >导入
          </importExcel>
        </el-button-group>
        <crud-toolbar
          :search.sync="crud.searchOptions.show"
          :compact.sync="crud.pageOptions.compact"
          :columns="crud.columns"
          @refresh="doRefresh()"
          @columns-filter-changed="handleColumnsFilterChanged"
        />
      </div>
<!--      <template slot="resourceSlot" slot-scope="scope">-->
<!--        <div class="demo-image__preview">-->
<!--          <el-image-->
<!--            v-for="item in scope.row.resource"-->
<!--            :src="item" :preview-src-list="scope.row.resource"-->
<!--            style="width: 50px; height: 50px; margin: 0 5px"-->
<!--            fit="fit">-->
<!--            <div slot="placeholder" class="image-slot">-->
<!--              加载中<span class="dot">...</span>-->
<!--            </div>-->
<!--          </el-image>-->
<!--        </div>-->
<!--      </template>-->
    </d2-crud-x>
    <!--  添加备注  -->
    <bug-record-list-dialog
      ref="recordList"
      :visible="recordListDialogVisible"
      @changeVisible="recordListDialogVisible=!recordListDialogVisible"
      :bugObj="this.selectedBugObj" />
    <new-record-dialog
      :visible="newRecordDialogVisible"
      @changeVisible="newRecordDialogVisible=!newRecordDialogVisible"
      :bugObj="this.selectedBugObj" />
    <solve-bug-dialog
      :visible="solveBugDialogVisible"
      :solution-options="dictionary('bug_solution')"
      :cause-reason-options="dictionary('bug_cause_reason')"
      @changeVisible="solveBugDialogVisible=!solveBugDialogVisible"
      :bugObj="this.selectedBugObj" />
    <close-bug-dialog
      :visible="closeBugDialogVisible"
      :solution-options="dictionary('bug_solution')"
      :cause-reason-options="dictionary('bug_cause_reason')"
      @changeVisible="closeBugDialogVisible=!closeBugDialogVisible"
      :bugObj="this.selectedBugObj" />
  </d2-container>
</template>

<script>
import * as api from './api'
import {crudOptions} from './crud'
import {d2CrudPlus} from 'd2-crud-plus'
import bugRecordListDialog from "@/views/custom/bug_killer/subDirectory/bugRecordListDialog.vue";
import newRecordDialog from "@/views/custom/bug_killer/subDirectory/newRecordDialog.vue";
import solveBugDialog from "@/views/custom/bug_killer/subDirectory/solveBugDialog.vue";
import closeBugDialog from "@/views/custom/bug_killer/subDirectory/closeBugDialog.vue";


export default {
  name: 'Index',
  mixins: [d2CrudPlus.crud],
  components: {
    bugRecordListDialog,
    newRecordDialog,
    solveBugDialog,
    closeBugDialog
  },
  data() {
    return {
      selectedBugObj: {},
      recordListDialogVisible: false,
      newRecordDialogVisible: false,
      solveBugDialogVisible: false,
      closeBugDialogVisible: false
    }
  },
  created() {
    this.getD2CrudTableData()
  },
  methods: {
    initAfter () {
      console.log('initAfter: ')
    },
    initColumnAfter (column) {
      console.log('initColumnAfter: ')
    },
    getCrudOptions() {
      return crudOptions(this)
    },
    pageRequest(query) {
      return api.GetBugList(query)
    },
    addRequest(row) {
      return api.AddBug(row)
    },
    updateRequest(row) {
      return api.UpdateBug(row)
    },
    delRequest(row) {
      return api.DelBug(row.id)
    },
    onExport() {
      const that = this
      this.$confirm('是否确认导出所有数据项?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(function () {
        const query = that.getSearch().getForm()
        return api.exportData({...query})
      })
    },
    onFetchRecordList(scope) {
      this.selectedBugObj = scope.row
      this.recordListDialogVisible = true
      this.$refs.recordList.fetchRecordList()
    },
    onAddNewRecord(scope) {
      this.selectedBugObj = scope.row
      this.newRecordDialogVisible = true
    },
    onSolveBug(scope) {
      this.selectedBugObj = scope.row
      this.solveBugDialogVisible = true
    },
    onCloseBug(scope) {
      this.selectedBugObj = scope.row
      this.closeBugDialogVisible = true
    }
  }
}
</script>
