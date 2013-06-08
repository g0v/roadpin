class CreateRoadCases < ActiveRecord::Migration
  def change
    create_table :road_cases do |t|
      t.integer :status, :default => 0
      t.integer :case_type, :default => 0
      t.text :raw_data
      t.date :start_on
      t.date :end_on

      t.timestamps
    end
  end
end
