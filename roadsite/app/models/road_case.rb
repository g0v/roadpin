class RoadCase < ActiveRecord::Base
  # attr_accessible :title, :body
  scope :digging, -> { where(['start_on <= ? AND end_on >= ?', Date.today, Date.today]) }

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
