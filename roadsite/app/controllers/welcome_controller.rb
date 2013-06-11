class WelcomeController < ApplicationController
  def index
    @day = params[:day].present? ? params[:day] : Date.today.strftime('%Y-%m-%d')
  end
end
