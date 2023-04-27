import {
  generateDict,
  generateForm,
  generateComponent,
  userColumns,
  bugSetColumns
} from "./extension";

import * as permission from "@/plugin/permission/directive/permission/permission";


export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: false //是否紧凑页面模式
    },
    options: {
      height: '100%',
      // tableType: 'vxe-table',
      // rowKey: true,
      rowId: 'id',
      lineEdit: {
        validation: true
      }
    },
    selectionRow: {
      align: 'center',
      width: 46
    },
    rowHandle: {
      width: 360,
      fixed: 'right',
      view: {
        thin: true,
        text: '',
        disabled() {return !vm.hasPermissions('Retrieve')}
      },
      edit: {
        thin: true,
        text: '',
        show() { return vm.hasPermissions('Update')},
        disabled() { return !vm.hasPermissions('Update')},
      },
      remove: {
        thin: true,
        text: '',
        show() {return vm.hasPermissions('Delete')},
        disabled() {return !vm.hasPermissions('Delete')}
      },
      custom: [
        {
          thin: true,
          size: 'small',
          icon: 'el-icon-s-operation',
          title: '操作日志',
          text: '',
          show() { return vm.hasPermissions('Retrieve') },
          disabled() { return !vm.hasPermissions('Retrieve') },
          emit: 'fetchRecords'
        },  {
          thin: true,
          size: 'small',
          type: 'warning',
          title: '解决问题',
          text: '解决',
          show() { return permission.is_rd() || permission.is_superuser() },
          disabled() { return !vm.hasPermissions('Update') },
          emit: 'solveBug'
        }, {
          thin: true,
          size: 'small',
          type: 'success',
          title: '关闭问题',
          text: '关闭',
          show() { return permission.is_qa() || permission.is_superuser() },
          disabled() { return !vm.hasPermissions('Update') },
          emit: 'closeBug'
        }, {
          thin: true,
          size: 'small',
          title: '备注信息',
          text: '备注',
          type: 'primary',
          show() { return vm.hasPermissions('Retrieve') },
          disabled() { return !vm.hasPermissions('Retrieve') },
          emit: 'addNewRecord'
        }
      ]
    },
    viewOptions: {
      componentType: 'form'  // form=使用表单组件,row=使用行展示组件
    },
    formOptions: {
      type: 'drawer',  // dialog or drawer
      defaultSpan: 24, // 默认的表单 span

    },
    indexRow: { // 或者直接传true,不显示title，不居中
      title: '序号',
      align: 'center',
      width: 60
    },
    columns: [
      {
        title: 'BUG合集',
        key: 'bug_set',
        search: {disabled: false},
        minWidth: 150,
        type: 'select',
        dict: generateDict('/api/custom/bug_set/', 'id', 'title'),
        form: generateForm(false, bugSetColumns(), false),
        component: generateComponent('bug_set_title', 'foreignKey', 'title')
      }, {
        title: 'bug标题',
        key: 'title',
        search: {
          disabled: false
        },
        minWidth: 240,
        form: {
          rules: [{required: true, message: 'title必填'}],
          component: {placeholder: '请输入'},
          itemProps: {class: {yxtInput: true}}
        }
      }, {
        title: 'bug描述',
        key: 'desc',
        search: { disabled: false},
        minWidth: 240,
        form: {
          component: {placeholder: '请输入'},
          itemProps: {class: {yxtInput: true}}
        }
      }, {
        title: '📎附件',
        key: 'resource',
        type: 'file-uploader',
        width: 340,
        form: {
          component: {
            props: {
              btnSize: 'small', // type=file-uploader时按钮的大小
              btnName: '选择文件',// type=file-uploader时按钮文字
              // accept: '.png', // 接受的文件后缀类型
              // suffix: '!200_200', //url后缀，用于图片样式处理，需要到对象存储平台配置样式
              type: 'form', // 当前使用哪种存储后端【cos/qiniu/alioss/form】
              elProps: { // 与el-uploader配置一致
                limit: 4 // 限制上传文件数量
              }
            }
          }
        }
      }, {
        title: '问题原因',
        key: 'cause_reason',
        minWidth: 120,
        type: 'select',
        dict: {data: vm.dictionary('bug_cause_reason')},
        search: { disabled: false },
        form: { value: 2 }
      }, {
        title: '严重级别',
        key: 'level',
        minWidth: 90,
        align: 'center',
        type: 'radio',
        dict: {data: vm.dictionary('bug_level')},
        search: {disabled: false},
        form: {
          disabled: false,
          value: 2
        }
      }, {
        title: 'bug状态',
        key: 'status',
        align: 'center',
        search: {disabled: false},
        minWidth: 120,
        type: 'select',
        dict: {data: vm.dictionary('bug_status')},
        form: { disabled: true, value: 1 }
      }, {
        title: '解决方案',
        key: 'solution',
        align: 'center',
        minWidth: 120,
        type: 'select',
        dict: {data: vm.dictionary('bug_solution')},
        form: {
          disabled: false,
          value: 1
        }
      }, {
        title: '跟进RD',
        key: 'follow_rd',
        search: {disabled: false},
        minWidth: 130,
        type: 'select',
        dict: generateDict('/api/system/user/', 'id', 'name'),
        form: generateForm(false, userColumns()),
        component: generateComponent('follow_rd_info', 'manyToMany', 'name')
      }, {
        title: '跟进QA',
        key: 'follow_qa',
        search: {disabled: false},
        minWidth: 130,
        type: 'select',
        dict: generateDict('/api/system/user/', 'id', 'name'),
        form: generateForm(false, userColumns()),
        component: generateComponent('follow_qa_info', 'manyToMany', 'name')
      }, {
        title: '问题关闭人',
        key: 'close_qa',
        type: 'select',
        search: {disabled: false},
        show() { return permission.is_admin() },
        minWidth: 130,
        dict: generateDict('/api/system/user/', 'id', 'name'),
        form: {disabled: true}, // generateForm(false, userColumns(), false)
        component: generateComponent('close_qa_name', 'foreignKey', 'name')
      }, {
        title: '归属RD',
        key: 'belong_rd',
        search: {disabled: false},
        minWidth: 130,
        type: 'select',
        show() { return permission.is_superuser() },
        dict: generateDict('/api/system/user/', 'id', 'name'),
        form: generateForm(false, userColumns(), false),
        component: generateComponent('belong_rd_name', 'foreignKey', 'name')
      }, {
        title: '归属团队',
        key: 'belong_dept',
        search: {disabled: false},
        minWidth: 130,
        type: 'select',
        show() { return permission.is_superuser() },
        dict: generateDict('/api/system/dept/', 'id', 'name'),
        form: {disabled: true}, //generateForm(false, deptColumns(), false),
        component: generateComponent('belong_dept_name', 'foreignKey', 'name')
      }, {
        title: '创建时间',
        minWidth: 150,
        key: 'create_datetime',
        type: 'datetime',
        form: {disabled: true}
      }, {
        title: '解决时间',
        key: 'solve_datetime',
        minWidth: 150,
        type: 'datetime',
        form: {disabled: true},
      }
    ]
  }
}
