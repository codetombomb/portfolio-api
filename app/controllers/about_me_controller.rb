class AboutMeController < ApplicationController
  def index
    traits = AboutMe.all
    render :json => traits, :except => [:id, :created_at, :updated_at]
  end
end
