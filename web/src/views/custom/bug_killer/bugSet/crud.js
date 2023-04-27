import {request} from "@/api/service";

export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true //是否紧凑页面模式
    },
    options: {
      height: '100%',
      // tableType: 'vxe-table',
      // rowKey: true,
      rowId: 'id',
      lineEdit:{
        validation:true //启用表单校验，性能会有一点影响
      }
    },
    selectionRow: {
      align: 'center',
      width: 46
    },
    rowHandle: {
      width: 150,
      fixed: 'right',
      view: {
        thin: true,
        text: '',
        disabled() { return !vm.hasPermissions('Retrieve') }
      },
      lineEdit: {
        thin: true,
        text: '',
        show() { return vm.hasPermissions('Update') },
        disabled() { return !vm.hasPermissions('Update') }
      },
      edit: {
        thin: true,
        text: '',
        show: false,
        disabled: false
      },
      remove: {
        thin: true,
        text: '',
        show() { return vm.hasPermissions('Delete') },
        disabled() { return !vm.hasPermissions('Delete') }
      },
      custom: []
    },
    viewOptions: {
      componentType: 'form'  // form=使用表单组件,row=使用行展示组件
    },
    formOptions: {
      type: 'drawer',  // dialog or drawer
      defaultSpan: 24 // 默认的表单 span
    },
    indexRow: { // 或者直接传true,不显示title，不居中
      title: '序号',
      align: 'center',
      width: 60
    },
    columns: [
      {
        title: '合集标题',
        key: 'title',
        minWidth: 120,
        search: {
          disabled: false
        },
        form: {
          disabled: false,
          rules: [ // 表单校验规则
            {
              required: true,
              message: 'related_prd_id必填'
            }
          ],
        }
      }, {
        title: '关联PRD编号',
        key: 'related_prd_id',
        search: {
          disabled: true
        },
        minWidth: 120,
        form: {
          rules: [ // 表单校验规则
            {
              required: true,
              message: 'related_prd_id必填'
            }
          ],
          component: {
            placeholder: '请输入'
          },
          itemProps: {
            class: {yxtInput: true}
          }
        }
      }, {
        title: '集合描述',
        key: 'desc',
        search: {
          disabled: false
        },
        minWidth: 240,
        form: {
          rules: [ // 表单校验规则
            {
              required: false,
              message: '选填必填'
            }
          ],
          component: {
            placeholder: '请输入'
          },
          itemProps: {
            class: {yxtInput: true}
          }
        }
      }, {
        title: '关联问题数',
        key: 'related_bug_cnt',
        search: { disabled: true },
        align: 'center',
        width: 90,
        form: {disabled: true}
      },
      {
        title: '创建时间',
        minWidth: 150,
        type: 'datetime',
        key: 'create_datetime',
        form: {
          disabled: true
        }
      }
    ]
  }
}
