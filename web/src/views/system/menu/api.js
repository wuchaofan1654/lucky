/*
 * @创建文件时间: 2021-06-01 22:41:21
 * @Auther: lucky
 * @最后修改人: lucky
 * @最后修改时间: 2021-07-29 19:23:33
 * 联系QQ:382503189
 * @文件介绍: 菜单管理接口
 */
import { request } from '@/api/service'

export const urlPrefix = '/api/system/menu/'

/**
 * 列表查询
 */
export function GetList (query) {
  return request({
    url: urlPrefix,
    method: 'get',
    params: { ...query }
  }).then(res => {
    // 将列表数据转换为树形数据
    return res
  })
}

/**
 * 新增
 */
export function createObj (obj) {
  return request({
    url: urlPrefix,
    method: 'post',
    data: obj
  })
}

/**
 * 修改
 */
export function UpdateObj (obj) {
  return request({
    url: urlPrefix + obj.id + '/',
    method: 'put',
    data: obj
  })
}

/**
 * 删除
 */
export function DelObj (id) {
  return request({
    url: urlPrefix + id + '/',
    method: 'delete',
    data: { id }
  })
}
