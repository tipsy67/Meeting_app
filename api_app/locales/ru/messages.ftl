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
conference-notification =
    { $text }?token={ $token }'>Перейти к конференции</a>.
    Лекция: <b>{ $lecture_name }</b>.
    Начало через: { $time_to_start }

conference-invitation =
    Вы приглашены на конференцию!
    Дата: <b>{ $date }</b> в <b>{ $time }</b>
    Спикер: { $speaker_name } { $speaker_username ->
        [null] { "" }
       *[other] (@{ $speaker_username })
    }
    Длительность: <b>{ $duration } минут</b>
    Ссылка: <a href={ $link }

### Форматы времени ###
time-duration =
    { $days ->
        [0] { "" }
        [1] 1 день
        [few] { $days } дня
       *[other] { $days } дней
    } { $hours ->
        [0] { $minutes } мин
        [1] 1 час { $minutes } мин
        [few] { $hours } часа { $minutes } мин
       *[other] { $hours } часов { $minutes } мин
    }