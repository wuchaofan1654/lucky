/*
 * @创建文件时间: 2021-06-27 10:14:26
 * @Auther: lucky
 * @最后修改人: lucky
 * @最后修改时间: 2021-07-27 23:00:10
 * 联系QQ:382503189
 * @文件介绍: 自定义指令-权限控制
 */
import permissionUtil from './util.permission'
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
