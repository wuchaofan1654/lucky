import { request} from '@/api/service'

export const urlPrefix = '/api/custom'


/**
 * bug_record列表查询
 */
export function GetBugRecordList (query) {
  query.limit = 999;
  return request({
    url: urlPrefix + '/bug_record',
    method: 'get',
    params: query
  })
}

/**
 * 新增bug_record
 */
export function AddBugRecord (obj) {
  return request({
    url: urlPrefix + '/bug_record/',
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
