/*
 * @创建文件时间: 2021-06-27 10:14:26
 * @Auther: lucky
 * @最后修改人: lucky
 * @最后修改时间: 2021-07-27 23:00:10
 * 联系QQ:382503189
 * @文件介绍: 自定义指令-权限控制
 */
import permissionUtil from './util.permission'
import state from "@/store/modules/d2admin/modules/user";

export default {
  inserted (el, binding, vnode) {
    const { value } = binding
    const hasPermission = permissionUtil.hasPermissions(value)
    if (process.env.VUE_APP_PM_ENABLED) {
      if (!hasPermission) {
        el.parentNode && el.parentNode.removeChild(el)
      }
    }
  }
}


const ROlE_ADMIN_TYPE = 1
const ROlE_PUBLIC_TYPE = 2
const ROlE_QA_TYPE = 3
const ROlE_IOS_TYPE = 4
const ROlE_ANDROID_TYPE = 5
const ROlE_SERVER_TYPE = 6
const ROlE_FE_TYPE = 7


export function is_superuser() {
  return state.state.info.is_superuser
}

export function is_admin() {
  return is_superuser() || state.state.info.role.includes(ROlE_ADMIN_TYPE)
}

export function is_public() {
  return state.state.info.role.includes(ROlE_PUBLIC_TYPE)
}

export function is_qa() {
  return state.state.info.role.includes(ROlE_QA_TYPE)
}

export function is_ios() {
  return state.state.info.role.includes(ROlE_IOS_TYPE)
}

export function is_android() {
  return state.state.info.role.includes(ROlE_ANDROID_TYPE)
}

export function is_server() {
  return state.state.info.role.includes(ROlE_SERVER_TYPE)
}

export function is_fe() {
  return state.state.info.role.includes(ROlE_FE_TYPE)
}

export function is_rd() {
  return is_ios() || is_android() || is_server() || is_fe()
}

