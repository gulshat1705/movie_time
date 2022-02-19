from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews
from django import forms


class MovieAdminForm(forms.ModelForm):


    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ['name',]                                 # при нажатии на name открывается

#admin.site.register(Category, CategoryAdmin) 1-вариант регистрации или с помощью декоратора

#                           1 -вариант
class ReviewInline(admin.StackedInline):                               # при открытии movie посмотреть отзывы
    model = Reviews
    extra = 1                                                           # количество дополнительных пустых полей 

#                                                                         2 -вариант поля выстраювается по горизонтали
class ReviewInline(admin.TabularInline):                                     # при открытии movie посмотреть отзывы
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email')


class MovieShotsInline(admin.TabularInline):                        # отображение кадры
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)


    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="50">')

    get_image.short_description = 'MovieShots Image'    


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ['name']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft',)
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')                     #'category__name' именно по каким категориям искать
    inlines = [MovieShotsInline, ReviewInline]                      # данный атрибут работает с повязками ForeignKey, ManyToMany
    save_on_top = True                                                # перенос кнопку save вверх
    save_as = True                                                     # при сохранении как новый объект , копируется появится новый объект
    list_editable = ('draft',)                                             # редактирование 
    actions = ['publish', 'unpublish']
    #fields = (('actors', 'directors', 'genres'), )  # ГРУППИРОВКА режиссеры и актеры в одну строку.но остальные поля исчезнут
    form = MovieAdminForm
    readonly_fields = ('get_image',)
    
    fieldsets = (           
        (None, {
            'fields': (('title', 'tagline'), )
        }),
        (None, {
            'fields': (('description', 'poster', 'get_image'), )
        }),
        (None, {
            'fields': (('year', 'world_premiere', 'country'), )
        }),
        ('Actors', {                                                         #скырть поля, там ссылка по ссылке открывается поля
            'classes': ('collapse',),
            'fields': (('actors', 'directors', 'genres', 'category'), )
        }),
        ('Budget', {
            'fields': (('budget', 'fees_in_usa', 'fees_in_world'), )
        }),
        ('Option', {
            'fields': (('url', 'draft'), )
        }),
    )
    
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="50" height="50">')


    
    def unpublish(self, request, queryset):
        """ снять с публикации """
        row_update = queryset.update(draft=True)
        if row_update == 1:
             message_bit = '1 запись была обновлена '
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')    


    def publish(self, request, queryset):
        """ опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
             message_bit = '1 запись была обновлена '
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')      

    publish.short_description = "опубликовать" 
    publish.allowed_permissions = ('change', )   

    unpublish.short_description = "снять с публикации" 
    unpublish.allowed_permissions = ('change', )   
          

    get_image.short_description = 'Poster'    


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')                                                      # только для чтения редактировать нельзя


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'get_image', )
    readonly_fields = ('get_image', )

    def get_image(self, obj):
       return mark_safe(f'<img src={obj.image.url} width="50" heght="60" ')

    get_image.short_description = 'Poster'


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'get_image')                            ##### get_image добавляем имя метода
    readonly_fields = ('get_image', )
    # отображение рисунка на админ панели 
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')               #!! from django.utils.safestring import mark_safe

    
    get_image.short_description = 'Image'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('ip', 'star', 'movie')


admin.site.register(RatingStar)

admin.site.site_title = "Web приложения Movie Time на Django"
admin.site.site_header = "Web приложения Movie Time на Django"