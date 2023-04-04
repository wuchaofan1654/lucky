/*
 * @创建文件时间: 2021-06-01 22:41:21
 * @Auther: lucky
 * @最后修改人: lucky
 * @最后修改时间: 2021-06-05 01:03:36
 * 联系QQ:382503189
 * @文件介绍: 角色管理接口
 */
import { request } from '@/api/service'

export const urlPrefix = '/api/system/role/'

export function GetList (query) {
  return request({
    url: urlPrefix,
    method: 'get',
    params: { ...query }
  })
}

export function GetObj (obj) {
  return request({
    url: urlPrefix + obj.id + '/',
    method: 'get'
  })
}

export function createObj (obj) {
  return request({
    url: urlPrefix,
    method: 'post',
    data: obj
  })
}

export function UpdateObj (obj) {
  return request({
    url: urlPrefix + obj.id + '/',
    method: 'put',
    data: obj
  })
}

export function DelObj (id) {
  return request({
    url: urlPrefix + id + '/',
    method: 'delete',
    data: { id }
  })
}
