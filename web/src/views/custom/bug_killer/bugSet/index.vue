<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x ref="d2Crud" v-bind="_crudProps" v-on="_crudListeners">
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
        </el-button-group>
        <crud-toolbar
          :search.sync="crud.searchOptions.show"
          :compact.sync="crud.pageOptions.compact"
          :columns="crud.columns"
          @refresh="doRefresh()"
          @columns-filter-changed="handleColumnsFilterChanged"
        />
      </div>
    </d2-crud-x>
  </d2-container>
</template>

<script>
import * as api from './api'
import {crudOptions} from './crud'
import {d2CrudPlus} from 'd2-crud-plus'

export default {
  name: 'Index',
  mixins: [d2CrudPlus.crud],
  data() {
    return {
      defaultProps: {
        children: 'children',
        label: 'title',
      }
    }
  },
  methods: {
    getCrudOptions() {
      return crudOptions(this)
    },
    pageRequest(query) {
      return api.GetBugSetList(query)
    },
    addRequest(row) {
      return api.AddBugSet(row).then(ret => { //改成返回{row}，要带上id
        row.id = ret.data
        return { row: row } //用于更新表格数据
      })
    },
    updateRequest(row) {
      return api.UpdateBugSet(row).then(ret => { // 改成返回 {row}
        return { row } //用于更新表格数据
      })
    },
    delRequest(row) {
      return api.DelBugSet(row.id)
    }
  }
}
</script>
