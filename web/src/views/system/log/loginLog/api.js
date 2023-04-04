/*
 * @创建文件时间: 2021-06-08 10:40:32
 * @Auther: lucky
 * @最后修改人: lucky
 * @最后修改时间: 2021-06-09 10:36:20
 * 联系QQ:382503189
 * @文件介绍: 操作日志
 */
import { request } from '@/api/service'

export const urlPrefix = '/api/system/login_log/'

export function GetList (query) {
  return request({
    url: urlPrefix,
    method: 'get',
    params: query
  })
}
