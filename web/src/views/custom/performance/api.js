import { downloadFile, request } from '@/api/service'

export const urlPrefix = '/api/custom/recording/'
/**
 * 列表查询
 */
export function GetList (query) {
  // query.limit = 999;
  return request({
    url: urlPrefix,
    method: 'get',
    params: query
  })
}

/**
 * 新增
 */
export function AddObj (obj) {
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

/**
 * 导出
 * @param params
 */
export function exportData (params) {
  return downloadFile({
    url: urlPrefix + 'export_data/',
    params: params,
    method: 'get'
  })
}
