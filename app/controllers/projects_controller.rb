class ProjectsController < ApplicationController
    def index
        projects = Project.all
        render :json => projects, :include => {:technologies => {:only => :tech}}, :except => [:created_at, :updated_at]
    end
end
