"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
import random
import sys


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._playlist_library = []
        self._current_play = None
        self._paused = None
        self._flagged = {}


    def number_of_videos(self):
        """Returns number of videos."""

        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")


    '''
    PART 1
    '''
    def show_all_videos(self):
        """Returns all videos."""

        print("Here's a list of all available videos:")
        videos = self._video_library.get_all_videos()
        newlist = sorted(videos, key=lambda x: x.title)
        for v in newlist:
            if (v.video_id not in self._flagged):
                print('\t', v.title, '('+v.video_id+')', '[%s]' % ' '.join(map(str, v.tags)))

            else:
                print('\t', v.title, '('+v.video_id+')', '[%s]' % ' '.join(map(str, v.tags)) + " - FLAGGED" + self._flagged[v.video_id])




    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        v_to_play = self._video_library.get_video(video_id)

        if(v_to_play and self._current_play == None):
            print("Playing video: " + v_to_play.title)
            self._current_play = v_to_play
            self._paused = None

        elif(self._current_play and v_to_play):
            print("Stopping video: " + self._current_play.title)
            print("Playing video: " + v_to_play.title)
            self._current_play = v_to_play
            self._paused = None

        elif(video_id in self._flagged):
            print("Cannot play video: Video is currently flagged" + self._flagged[video_id] )

        else:
            print("Cannot play video: Video does not exist")


    def stop_video(self):
        """Stops the current video."""

        if(self._current_play):  
            print("Stopping video: " + self._current_play.title)
            self._current_play = None

        else:
            print("Cannot stop video: No video is currently playing")


    def play_random_video(self):
        """Plays a random video from the video library."""
        v_allowed = [v for v in self._video_library.get_all_videos() if v.video_id not in self._flagged]

        if(len(v_allowed) == 0):
            print("No videos available")

        else:
            v_to_play = random.choice(v_allowed)

            if(self._current_play):  
                print("Stopping video: " + self._current_play.title)
                self._current_play = v_to_play
                self._paused = None
                print("Playing video: " + v_to_play.title)

            else:
                self._current_play = v_to_play
                self._paused = None
                print("Playing video: " + v_to_play.title)


    def pause_video(self):
        """Pauses the current video."""

        if(self._current_play and self._paused == None):  
            self._paused = self._current_play
            print("Pausing video: " + self._current_play.title)

        elif(self._current_play == None):
            print("Cannot pause video: No video is currently playing")

        else:   
            print("Video already paused: " + self._paused.title)


    def continue_video(self):
        """Resumes playing the current video."""

        if(self._current_play and self._paused):
            print("Continuing video: " + self._current_play.title)
            self._paused = None

        elif(self._current_play and self._paused == None):
            print("Cannot continue video: Video is not paused")

        elif(self._current_play == None):
            print("Cannot continue video: No video is currently playing")


    def show_playing(self):
        """Displays video currently playing."""

        if(self._current_play and self._paused):
            print("Currently playing:", self._current_play.title, '('+self._current_play.video_id+')', '[%s]' % ' '.join(map(str, self._current_play.tags)), "- PAUSED")

        elif(self._current_play == None):
            print("No video is currently playing")

        elif(self._current_play and self._paused == None):
            print("Currently playing:", self._current_play.title, '('+self._current_play.video_id+')', '[%s]' % ' '.join(map(str, self._current_play.tags)))


    '''
    PART 2
    '''
    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if (' ' in playlist_name):
            print("Playlist name cannot contain space")

        pl = [item for item in self._playlist_library if item.name.lower() == playlist_name.lower()]
            
        if(len(pl) == 1):
            print("Cannot create playlist: A playlist with the same name already exists")

        else:
            print("Successfully created new playlist: "+ playlist_name)
            self._playlist_library.append(Playlist(playlist_name))


    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        vid_to_add = self._video_library.get_video(video_id)
        pl = [item for item in self._playlist_library if item.name.lower() == playlist_name.lower()]

        if(vid_to_add == None):
            if(len(pl) == 1):
                print("Cannot add video to " + playlist_name + ": Video does not exist")

            else:
                print("Cannot add video to " + playlist_name + ": Playlist does not exist")

        elif(video_id in self._flagged):
            print("Cannot add video to " + playlist_name + ": Video is currently flagged" + self._flagged[video_id])

        else:            
            if(len(pl) == 1):
                vids = [v for v in pl[0]._listed_vids if v.video_id == video_id]

                if (len(vids) == 0): 
                    pl[0]._listed_vids.append(vid_to_add)
                    print("Added video to " + playlist_name + ": " + vid_to_add.title)

                elif(video_id in self._flagged):
                    print("Cannot add video to " + playlist_name + ": Video is currently flagged" + self._flagged[video_id])

                else:
                    print("Cannot add video to " + playlist_name + ": Video already added")

            else:
                print("Cannot add video to " + playlist_name + ": Playlist does not exist")



    def show_all_playlists(self):
        """Display all playlists."""

        if(len(self._playlist_library) == 0):
            print("No playlists exist yet")
        
        else:
            newlist = sorted(self._playlist_library, key=lambda x: x.name)
            print("Showing all playlists:")
            for pl in newlist:
                print('\t', pl.name)



    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        pl = [item for item in self._playlist_library if item.name.lower() == playlist_name.lower()]
            
        if(len(pl) == 1):
            print("Showing playlist: " + playlist_name)
            vids = pl[0]._listed_vids
            if (len(vids) == 0): 
                print('\t', "No videos here yet")

            else:
               for i in range(0, len(vids)):
                    if(vids[i].video_id not in self._flagged):
                        print('\t', vids[i].title, '('+vids[i].video_id+')', '[%s]' % ' '.join(map(str, vids[i].tags)))

                    else: 
                        print('\t', vids[i].title, '('+vids[i].video_id+')', '[%s]' % ' '.join(map(str, vids[i].tags)) + " - FLAGGED" + self._flagged[vids[i].video_id])



        else:
            print("Cannot show playlist " + playlist_name + ": Playlist does not exist")


    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        vid_to_remove = self._video_library.get_video(video_id)
        pl = [item for item in self._playlist_library if item.name.lower() == playlist_name.lower()]
            
        if(len(pl) == 1):
            vids = [v for v in pl[0]._listed_vids if v.video_id == video_id]

            if len(vids) == 1:
                pl[0]._listed_vids = [v for v in pl[0]._listed_vids if v.video_id != video_id]
                print("Removed video from " + playlist_name + ": " + vids[0].title)

            else:
                if(vid_to_remove): 
                    print("Cannot remove video from " + playlist_name + ": Video is not in playlist")

                else:
                    print("Cannot remove video from " + playlist_name + ": Video does not exist")

        else:
            print("Cannot remove video from " + playlist_name + ": Playlist does not exist")


    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        pl = [item for item in self._playlist_library if item.name.lower() == playlist_name.lower()]
            
        if(len(pl) == 1):
            pl[0]._listed_vids.clear()
            print("Successfully removed all videos from "+ playlist_name)

        else:
            print("Cannot clear playlist " + playlist_name + ": Playlist does not exist")


    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        pl = [item for item in self._playlist_library if item.name.lower() == playlist_name.lower()]
            
        if(len(pl) == 1):
            self._playlist_library = [item for item in self._playlist_library if item.name.lower() != playlist_name.lower()]
            print("Deleted playlist: " + playlist_name)

        else:
            print("Cannot delete playlist " + playlist_name + ": Playlist does not exist")


    '''
    PART 3
    '''
    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        vids = [v for v in self._video_library.get_all_videos() if search_term.lower() in v.title.lower()]
        
        vids_not_flagged = [v for v in vids if v.video_id not in self._flagged]

        if len(vids_not_flagged) == 0:
            print("No search results for " + search_term)

        else:
            newlist = sorted(vids_not_flagged, key=lambda x: x.title)
            print("Here are the results for " + search_term + ":")
            for i in range (0, len(newlist)):
                print(str(i+1) +') '+ newlist[i].title + ' ('+newlist[i].video_id+')', '[%s]' % ' '.join(map(str, newlist[i].tags)) )

            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")

            usr_number = input()
            if (usr_number.isdigit() and int(usr_number) <= len(newlist) and int(usr_number) > 0):
                self.play_video(newlist[int(usr_number)-1].video_id)


    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        vids_tag = [v for v in self._video_library.get_all_videos() if video_tag.lower() in v.tags]
        vids_not_flagged = [v for v in vids_tag if v.video_id not in self._flagged]

        if len(vids_not_flagged) == 0:
            print("No search results for " + video_tag)

        else:
            newlist = sorted(vids_not_flagged, key=lambda x: x.title)
            print("Here are the results for " + video_tag + ":")
            for i in range (0, len(newlist)):
                print(str(i+1) +') '+ newlist[i].title + ' ('+newlist[i].video_id+')', '[%s]' % ' '.join(map(str, newlist[i].tags)) )

            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")

            usr_number = input()
            if (usr_number.isdigit() and int(usr_number) <= len(newlist) and int(usr_number) > 0):
                self.play_video(newlist[int(usr_number)-1].video_id)



    '''
    PART 4 (Extra)
    '''
    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        v_to_flag = self._video_library.get_video(video_id)

        if(v_to_flag):
            if(video_id in self._flagged):
                print("Cannot flag video: Video is already flagged")

            else:
                if(len(flag_reason) > 0):
                    self._flagged[video_id] = " (reason: " + flag_reason + ")"
                    print("Successfully flagged video: " + v_to_flag.title + self._flagged[video_id])
                
                else:
                    self._flagged[video_id] = " (reason: Not supplied)"
                    print("Successfully flagged video: " + v_to_flag.title + self._flagged[video_id])

        elif(v_to_flag == self._current_play and v_to_flag):
            if(len(flag_reason) > 0):
                self._flagged[video_id] = " (reason: " + flag_reason + ")"
                self.stop_video()
                print("Successfully flagged video: " + v_to_flag.title + self._flagged[video_id])
                
            else:
                self._flagged[video_id] = " (reason: Not supplied)"
                self.stop_video()
                print("Successfully flagged video: " + v_to_flag.title + self._flagged[video_id])


        else:
            print("Cannot flag video: Video does not exist")


    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        v_to_unflag = self._video_library.get_video(video_id)

        if(v_to_unflag):
            if(video_id not in self._flagged):
                print("Cannot remove flag from video: Video is not flagged")

            else:
                self._flagged.pop(video_id)
                print("Successfully removed flag from video: " + v_to_unflag.title)

        else:
            print("Cannot remove flag from video: Video does not exist")
