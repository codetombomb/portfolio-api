class AboutMeController < ApplicationController
  def index
    traits = AboutMe.all
    render :json => traits
  end
end
