broadcast_test = {
    'kind': 'youtube#liveBroadcast', 
    'etag': '4bPEuNrfInHnEs8VzwTTXW9uRcI', 
    'id': 'i7IfCL1365Y', 
    'snippet': {
        'publishedAt': '2025-07-03T19:25:50Z', 
        'channelId': 'UCelUWHdQIPCRPugT84x4Luw', 
        'title': 'async test', 
        'description': '', 
        'thumbnails': {
            'default': {
                'url': 'https://i.ytimg.com/vi/i7IfCL1365Y/default_live.jpg', 
                'width': 120, 
                'height': 90
                }, 
            'medium': {
                'url': 'https://i.ytimg.com/vi/i7IfCL1365Y/mqdefault_live.jpg', 
                'width': 320, 
                'height': 180
                }, 
            'high': {
                'url': 'https://i.ytimg.com/vi/i7IfCL1365Y/hqdefault_live.jpg', 
                'width': 480, 
                'height': 360
                }
            }, 
            'scheduledStartTime': '2025-07-03T21:25:49Z', 
            'isDefaultBroadcast': False, 
            'liveChatId': 'KicKGFVDZWxVV0hkUUlQQ1JQdWdUODR4NEx1dxILaTdJZkNMMTM2NVk'
        }, 
    'status': {
        'lifeCycleStatus': 'created', 
        'privacyStatus': 'unlisted', 
        'recordingStatus': 'notRecording', 
        'madeForKids': False, 
        'selfDeclaredMadeForKids': False
        }, 
    'contentDetails': {
        'monitorStream': {
            'enableMonitorStream': True, 
            'broadcastStreamDelayMs': 0, 
            'embedHtml': '<iframe width="425" height="344" src="https://www.youtube.com/embed/i7IfCL1365Y?autoplay=1&livemonitor=1" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'
            }, 
        'enableEmbed': False, 
        'enableDvr': True, 
        'enableContentEncryption': False, 
        'recordFromStart': True, 
        'enableClosedCaptions': False, 
        'closedCaptionsType': 'closedCaptionsDisabled', 
        'enableLowLatency': False, 
        'latencyPreference': 'normal', 
        'projection': 'rectangular', 
        'enableAutoStart': False, 
        'enableAutoStop': False
        }
    }

stream_test = {
    'kind': 'youtube#liveStream', 
    'etag': 'P-xqpURcsKGYnLsUUkI3JZo7XNg', 
    'id': 'elUWHdQIPCRPugT84x4Luw1751574571393505', 
    'snippet': {
        'publishedAt': '2025-07-03T20:29:31Z', 
        'channelId': 'UCelUWHdQIPCRPugT84x4Luw', 
        'title': 'async test stream', 
        'description': '', 
        'isDefaultStream': False
        }, 
    'cdn': {
        'ingestionType': 'rtmp', 
        'ingestionInfo': {
            'streamName': 'bkf9-ahwj-asgu-dqgv-08j1', 
            'ingestionAddress': 'rtmp://a.rtmp.youtube.com/live2', 
            'backupIngestionAddress': 'rtmp://b.rtmp.youtube.com/live2?backup=1', 
            'rtmpsIngestionAddress': 'rtmps://a.rtmps.youtube.com/live2', 
            'rtmpsBackupIngestionAddress': 'rtmps://b.rtmps.youtube.com/live2?backup=1'
            }, 
        'resolution': '720p', 
        'frameRate': '30fps'
        }, 
    'status': {
        'streamStatus': 'ready', 
        'healthStatus': {
            'status': 'noData'
            }
        }, 
    'contentDetails': {
        'closedCaptionsIngestionUrl': 'http://upload.youtube.com/closedcaption?cid=bkf9-ahwj-asgu-dqgv-08j1', 
        'isReusable': True
        }
    }

broadcast_bind = {'kind': 'youtube#liveBroadcast', 'etag': 'tBfuynSPot5dOQEIhM1Yn_VpPAc', 'id': 'i7IfCL1365Y', 'snippet': {'publishedAt': '2025-07-03T19:25:50Z', 'channelId': 'UCelUWHdQIPCRPugT84x4Luw', 'title': 'async test', 'description': '', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/i7IfCL1365Y/default_live.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/i7IfCL1365Y/mqdefault_live.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/i7IfCL1365Y/hqdefault_live.jpg', 'width': 480, 'height': 360}, 'standard': {'url': 'https://i.ytimg.com/vi/i7IfCL1365Y/sddefault_live.jpg', 'width': 640, 'height': 480}, 'maxres': {'url': 'https://i.ytimg.com/vi/i7IfCL1365Y/maxresdefault_live.jpg', 'width': 1280, 'height': 720}}, 'scheduledStartTime': '2025-07-03T21:25:49Z', 'isDefaultBroadcast': False, 'liveChatId': 'KicKGFVDZWxVV0hkUUlQQ1JQdWdUODR4NEx1dxILaTdJZkNMMTM2NVk'}, 'status': {'lifeCycleStatus': 'ready', 'privacyStatus': 'unlisted', 'recordingStatus': 'notRecording', 'madeForKids': False, 'selfDeclaredMadeForKids': False}, 'contentDetails': {'boundStreamId': 'elUWHdQIPCRPugT84x4Luw1751574571393505', 'boundStreamLastUpdateTimeMs': '2025-07-03T20:29:31Z', 'monitorStream': {'enableMonitorStream': True, 'broadcastStreamDelayMs': 0, 'embedHtml': '<iframe width="425" height="344" src="https://www.youtube.com/embed/i7IfCL1365Y?autoplay=1&livemonitor=1" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'}, 'enableEmbed': False, 'enableDvr': True, 'enableContentEncryption': False, 'recordFromStart': True, 'enableClosedCaptions': False, 'closedCaptionsType': 'closedCaptionsDisabled', 'enableLowLatency': False, 'latencyPreference': 'normal', 'projection': 'rectangular', 'enableAutoStart': False, 'enableAutoStop': False}}

last_broadcast = {'kind': 'youtube#liveBroadcast', 'etag': 'D20c-6nIHb72Ffqk0whbI6MuNWg', 'id': 'Apx5zJa79_Y', 'snippet': {'publishedAt': '2025-07-03T22:12:11Z', 'channelId': 'UCelUWHdQIPCRPugT84x4Luw', 'title': 'test with auto start', 'description': '', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/Apx5zJa79_Y/default_live.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/Apx5zJa79_Y/mqdefault_live.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/Apx5zJa79_Y/hqdefault_live.jpg', 'width': 480, 'height': 360}}, 'scheduledStartTime': '2025-07-03T22:30:48Z', 'isDefaultBroadcast': False, 'liveChatId': 'KicKGFVDZWxVV0hkUUlQQ1JQdWdUODR4NEx1dxILQXB4NXpKYTc5X1k'}, 'status': {'lifeCycleStatus': 'created', 'privacyStatus': 'unlisted', 'recordingStatus': 'notRecording', 'selfDeclaredMadeForKids': False}, 'contentDetails': {'monitorStream': {'enableMonitorStream': True, 'broadcastStreamDelayMs': 0, 'embedHtml': '<iframe width="425" height="344" src="https://www.youtube.com/embed/Apx5zJa79_Y?autoplay=1&livemonitor=1" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'}, 'enableEmbed': False, 'enableDvr': True, 'enableContentEncryption': False, 'recordFromStart': True, 'enableClosedCaptions': False, 'closedCaptionsType': 'closedCaptionsDisabled', 'enableLowLatency': False, 'latencyPreference': 'normal', 'projection': 'rectangular', 'enableAutoStart': True, 'enableAutoStop': True}}