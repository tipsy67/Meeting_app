### Общие сообщения ###
attention-message = Внимание, { $recipient_name }!
    { $text } { $initiator_name ->
        [null] { "" }
       *[other]  { $initiator_name } { $initiator_username ->
            [null] { "" }
           *[other] (@{ $initiator_username })
        }
    }

subscribe = На вас подписался
unsubscribe = От вас отписался

add_to_lecture = добавил вас в лекцию
remove_from_lecture = удалил вас из лекции

welcome-notification =
    Здравствуйте,  $first_name } { $last_name ->
        [null] { "" }
       *[other] { $last_name }
    }{ $username ->
        [null] { "" }
       *[other] (@{ $username })
    }!


### Уведомления о конференции ###
conference-invitation =
    Вы приглашены на конференцию!
    Дата: <b>{ $date }</b> в <b>{ $time }</b>
    Спикер: { $speaker_name } { $speaker_username ->
        [null] { "" }
       *[other] (@{ $speaker_username })
    }
    Лекция: <b>{ $lecture_name }</b>.
    Начало через: { $time_to_start }
    Длительность: <b>{ $duration } минут</b>
    Ссылка: <a href='{ $link }?token={ $token }'>Перейти к конференции</a>.

conference-speaker =
    Напоминаем о конференции!
    Дата: <b>{ $date }</b> в <b>{ $time }</b>
    Лекция: <b>{ $lecture_name }</b>.
    Начало через: { $time_to_start }
    Длительность: <b>{ $duration } минут</b>
    Ссылка: <a href='{ $link }'>Перейти к конференции</a>.

### Форматы времени ###
time-duration =
    { $days ->
        [0] { "" }
        [1] 1 день
        [few] { $days } дня
       *[other] { $days } дней
    } { $hours ->
        [0] { "" }
        [1] 1 час
        [few] { $hours } часа
       *[other] { $hours } часов
    } { $minutes ->
        [0] { "" }
       *[other] { $minutes } мин
    }