
export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      // tableType: 'vxe-table',
      // rowKey: true,
      rowId: 'id'
    },
    selectionRow: {
      align: 'center',
      width: 46
    },
    rowHandle: {
      width: 240,
      fixed: 'right',
      view: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      edit: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Delete')
        }
      },
      custom: [
      ]
    },
    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 12 // 默认的表单 span
    },
    indexRow: { // 或者直接传true,不显示title，不居中
      title: '序号',
      align: 'center',
      width: 60
    },
    columns: [
      {
        title: 'Host',
        key: 'host',
        width: 180,
        form: {
          rules: [ // 表单校验规则
            {
              required: true,
              message: 'host必填'
            }
          ],
          component: {
            placeholder: '请输入host'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: 'Path',
        key: 'path',
        width: 180,
        form: {
          rules: [ // 表单校验规则
            {
              required: true,
              message: '路径必填'
            }
          ],
          component: {
            placeholder: '请输入url路径'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '唯一标识名称',
        key: 'unique_name',
        width: 180,
        form: {
          disabled: true
        }
      },
      {
        title: '请求参数',
        key: 'request_meta',
        form: {
          disabled: true
        }
      },
      {
        title: '响应信息',
        key: 'response_meta',
        form: {
          disabled: true
        }
      },
      {
        title: '创建时间',
        key: 'create_datetime',
        width: 150,
        form: {
          disabled: true
        }
      }
    ]
  }
}
