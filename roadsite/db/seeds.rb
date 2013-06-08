# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rake db:seed (or created alongside the db with db:setup).
#
# Examples:
#
#   cities = City.create([{ name: 'Chicago' }, { name: 'Copenhagen' }])
#   Mayor.create(name: 'Emanuel', city: cities.first)
@files = Dir.glob("#{Rails.root}/doc/case/*.json")
for file in @files
  cases = JSON.parse(File.read(file))
  cases.each do |data|
    ret = {}
    matches = /(?<sy>\d+)\/(?<sm>\d+)\/(?<sd>\d+)~(?<ey>\d+)\/(?<em>\d+)\/(?<ed>\d+)/.match(data['WORK_DATEpro'])
    if matches
      ret[:start_on] = Date.parse("#{matches[:sy].to_i + 1911}/#{matches[:sm]}/#{matches[:sd]}")
      ret[:end_on] = Date.parse("#{matches[:ey].to_i + 1911}/#{matches[:em]}/#{matches[:ed]}")
    else
      next
    end
    ret[:status] = data['CASE_STATUSpro'].to_i
    ret[:case_type] = data['CASE_TYPEpro'].to_i
    ret[:raw_data] = data.to_json
    RoadCase.create(ret)
  end
end
