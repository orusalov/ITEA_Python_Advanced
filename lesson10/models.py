import mongoengine as ME
ME.connect(db='TestUsers', host='127.0.0.1', port=27017)


class UserLikes(ME.EmbeddedDocument):

    name = ME.StringField(min_length=2, max_length=255)
    quantity = ME.IntField(min_value=0)


class User(ME.Document):
    name = ME.StringField(min_length=2, max_length=255)
    login = ME.StringField(max_length=255, min_length=3, unique=True)
    password = ME.StringField(min_length=10, max_length=1024)
    interests = ME.ListField(ME.StringField())
    likes = ME.EmbeddedDocumentField(UserLikes)

    def __str__(self):
        return f'{self.id} {self.name}'


if __name__ == '__main__':
    # for i in range(5):
    #     user = User(name=f'Johnksd{i}', login=f'John{i}', password='al;sdlasd;', interests=['Foo'])
    #     user.save()
    # like = UserLikes(name='Ann', quantity=4)
    users = User.objects.get(name='Ьшсрфуд')
    # user = User(name=f'Ьшсрфуд', login=f'Зцв', password='al;sddsadlasd;', interests=['Films'], likes=like).save()
    print(users.to_json())