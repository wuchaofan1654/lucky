import {downloadFile, request} from '@/api/service'

export const urlPrefix = '/api/custom'

/**
 * bug列表查询
 */
export function GetBugList (query) {
  return request({
    url: urlPrefix + '/bug/',
    method: 'get',
    params: query
  })
}

/**
 * 新增bug
 */
export function AddBug (obj) {
  return request({
    url: urlPrefix + '/bug/',
    method: 'post',
    data: obj
  })
}

/**
 * 修改bug
 */
export function UpdateBug (obj) {
  return request({
    url: urlPrefix + '/bug/' + obj.id + '/',
    method: 'put',
    data: obj
  })
}

/**
 * 删除bug
 */
export function DelBug (id) {
  return request({
    url: urlPrefix + '/bug' + id + '/',
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
    url: urlPrefix + '/bug/export_data/',
    params: params,
    method: 'get'
  })
}

/**
 * bug_record列表查询
 */
export function GetBugRecordList (query) {
  // query.limit = 999;
  return request({
    url: urlPrefix + '/bug_record',
    method: 'get',
    params: query
  })
}

/**
 * 新增bug_record
 */
export function AddBugSetRecord (obj) {
  return request({
    url: urlPrefix + '/bug_record',
    method: 'post',
    data: obj
  })
}

/**
 * 修改bug_record
 */
export function UpdateBugRecord (obj) {
  return request({
    url: urlPrefix + '/bug_record' + obj.id + '/',
    method: 'put',
    data: obj
  })
}

/**
 * 删除bug_record
 */
export function DelBugRecord (id) {
  return request({
    url: urlPrefix + '/bug_record' + id + '/',
    method: 'delete',
    data: { id }
  })
}
