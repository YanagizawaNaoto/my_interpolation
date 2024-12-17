import cv2
import os

class DanceFrameDataset:
    def __init__(self):
        # ファイルが配置されているディレクトリを基準に input_video を設定
        script_dir = os.path.dirname(os.path.abspath(__file__))  # スクリプトの配置ディレクトリ
        self.video_dir = os.path.join(script_dir, "input_video")
        
        # video_dir 内の .mp4 ファイルパスを取得
        if os.path.exists(self.video_dir) and os.path.isdir(self.video_dir):
            self.video_paths = [os.path.join(self.video_dir, f) for f in os.listdir(self.video_dir) if f.endswith('.mp4')]
        else:
            print(f"Directory {self.video_dir} does not exist or is not a directory.")
            self.video_paths = []
        
    def extract_frames(self, output_dir):
        for video_path in self.video_paths:
            cap = cv2.VideoCapture(video_path)
            
            # 動画のFPSを自動取得
            fps = cap.get(cv2.CAP_PROP_FPS)
            if fps == 0:  # FPSが取得できない場合のエラー処理
                print(f"Unable to determine FPS for video: {video_path}")
                continue
            
            # フレーム間隔を計算
            frame_interval = int(fps // 10)  # 0.1秒間隔
            middle_interval = frame_interval // 2  # 0.05秒間隔
            
            # フレーム総数を取得
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            current_frame = 0
            
            while current_frame < frame_count - frame_interval:
                # フレーム1（開始フレーム）
                cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
                ret1, frame1 = cap.read()
                
                # フレーム2（中間フレーム - 目標）
                cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame + middle_interval)
                ret2, frame_target = cap.read()
                
                # フレーム3（終了フレーム）
                cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame + frame_interval)
                ret3, frame2 = cap.read()
                
                if ret1 and ret2 and ret3:
                    # フレームを保存
                    frame_set_dir = os.path.join(output_dir, f'sequence_{current_frame}')
                    os.makedirs(frame_set_dir, exist_ok=True)
                    
                    cv2.imwrite(os.path.join(frame_set_dir, 'frame1.jpg'), frame1)
                    cv2.imwrite(os.path.join(frame_set_dir, 'target.jpg'), frame_target)
                    cv2.imwrite(os.path.join(frame_set_dir, 'frame2.jpg'), frame2)
                
                current_frame += frame_interval
            
            cap.release()
