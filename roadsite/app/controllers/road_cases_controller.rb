class RoadCasesController < ApplicationController

  def index
    ret = [];
    day = params[:day].present? ? params[:day] : Date.today.strftime('%Y-%m-%d')

    cases = case day
    when 'all' then RoadCase.digging
    else RoadCase.available.day(Date.parse(day))
    end

    cases.each do |r|
      ret << r.to_hash
    end

    render :json => ret.to_json
  end
end
