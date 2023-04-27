
import {request} from "@/api/service";

export function userColumns() {
  return [
    {filed: 'id', title: '用户ID'},
    {filed: 'name', title: '用户名'}
  ]
}

export function fileColumns() {
  return [
    {filed: 'id', title: '文件ID'},
    {filed: 'url', title: '文件url'}
  ]
}

export function deptColumns() {
  return [
    {filed: 'id', title: '部门ID'},
    {filed: 'name', title: '部门名'}
  ]
}

export function bugSetColumns() {
  return [
    {filed: 'id', title: '合集ID'},
    {filed: 'title', title: '合集名称'}
  ]
}


export function generateDict(url, value, label) {
  return {
    cache: false,
    url: url,
    value: value, // 数据字典中value字段的属性名
    label: label, // 数据字典中label字段的属性名
    getData: (url, dict, {
      form,
      component
    }) => {
      return request({
        url: url,
        params: {
          page: 1,
          limit: 10
        }
      }).then(ret => {
        component._elProps.page = ret.data.page
        component._elProps.limit = ret.data.limit
        component._elProps.total = ret.data.total
        return ret.data.data
      })
    }
  }
}


export function generateForm(required=false, columns=[], multiple=true) {
  return {
    rules: [ // 表单校验规则
      {
        required: required,
        message: '必填项'
      }
    ],
    itemProps: {
      class: {yxtInput: true}
    },
    component: {
      span: 18,
      pagination: false,
      props: {multiple: multiple},
      elProps: {
        columns: columns
      }
    }
  }
}


export function generateComponent(valueBinding, name='manyToMany', children='name') {
  return {
    name: name,
    valueBinding: valueBinding,
    children: children,
    span: 24
  }
}
