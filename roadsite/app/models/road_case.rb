# encoding: UTF-8
class RoadCase < ActiveRecord::Base
  # attr_accessible :title, :body
  scope :digging, -> { where(['start_on <= ? AND end_on >= ?', Date.today, Date.today]) }
  scope :available, -> { where(['status = ? OR status = ?', 3, 5]) }
  scope :day, ->(day){ where(['start_on <= ? AND end_on >= ?', day, day]) }

  def human_status
    case status
    when 0 then "未成案"
    when 1 then "計畫案件"
    when 2 then "設計"
    when 3 then "施工"
    when 4 then "結案"
    when 5 then "竣工保固"
    when 9 then "取消中止"
    else ""
    end
  end

  def region
    json_data["REG_NAMEpro"]
  end

  def location
    json_data["CASE_LOCATIONpro"]
  end

  def range
    json_data['CASE_RANGEpro']
  end

  def ctr_wname
    json_data['CTR_WNAMEpro']
  end

  def ctr_oname
    json_data['CTR_ONAMEpro']
  end

  def dt_result
    json_data['dtResultpro']
  end

  def to_hash
    {
      :human_status => human_status,
      :case_type => case_type,
      :start_on => start_on.strftime('%Y-%m-%d'),
      :end_on => end_on.strftime('%Y-%m-%d'),
      :region => region,
      :location => location,
      :range => range,
      :ctr_wname => ctr_wname,
      :ctr_oname => ctr_oname,
      :dt_result => dt_result
    }
  end

  private
  def json_data
    @json_data ||= JSON.parse(raw_data)
  end
end
