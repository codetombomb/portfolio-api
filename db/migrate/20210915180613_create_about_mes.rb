class CreateAboutMes < ActiveRecord::Migration[6.1]
  def change
    create_table :about_mes do |t|
      t.string :trait

      t.timestamps
    end
  end
end
