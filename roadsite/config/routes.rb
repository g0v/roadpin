Roadsite::Application.routes.draw do
  root :to => 'welcome#index'

  resources :road_cases
end
