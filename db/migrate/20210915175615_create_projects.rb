class CreateProjects < ActiveRecord::Migration[6.1]
  def change
    create_table :projects do |t|
      t.string :title
      t.text :description
      t.string :img_name
      t.string :youtube_link
      t.string :github_link

      t.timestamps
    end
  end
end
