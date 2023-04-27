import {downloadFile, request} from '@/api/service'

export const urlPrefix = '/api/custom'
/**
 * bug_set列表查询
 */
export function GetBugSetList (query) {
  // query.limit = 999;
  return request({
    url: urlPrefix + '/bug_set/',
    method: 'get',
    params: query
  })
}

/**
 * 新增bug_set
 */
export function AddBugSet (obj) {
  return request({
    url: urlPrefix + '/bug_set/',
    method: 'post',
    data: obj
  })
}

/**
 * 修改bug_set
 */
export function UpdateBugSet (obj) {
  return request({
    url: urlPrefix + '/bug_set/' + obj.id + '/',
    method: 'put',
    data: obj
  })
}

/**
 * 删除bug_set
 */
export function DelBugSet (id) {
  return request({
    url: urlPrefix + '/bug_set/' + id + '/',
    method: 'delete',
    data: { id }
  })
}
