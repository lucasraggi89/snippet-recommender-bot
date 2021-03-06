import sys
sys.path.append('../..')
from code_identifier.src.common import Config, VocabType
from argparse import ArgumentParser
from code_identifier.src.interactive_predict import InteractivePredictor
from code_identifier.src.model import Model


def main(raw_args=None):
    parser = ArgumentParser()
    parser.add_argument("-d", "--data", dest="data_path",
                        help="path to preprocessed dataset", required=False)
    parser.add_argument("-te", "--test", dest="test_path",
                        help="path to test file", metavar="FILE", required=False)

    is_training = '--train' in sys.argv or '-tr' in sys.argv
    parser.add_argument("-s", "--save", dest="save_path",
                        help="path to save file", metavar="FILE", required=False)
    parser.add_argument("-w2v", "--save_word2v", dest="save_w2v",
                        help="path to save file", metavar="FILE", required=False)
    parser.add_argument("-t2v", "--save_target2v", dest="save_t2v",
                        help="path to save file", metavar="FILE", required=False)
    parser.add_argument("-l", "--load", dest="load_path",
                        help="path to save file", metavar="FILE", required=False)
    parser.add_argument('--save_w2v', dest='save_w2v', required=False,
                        help="save word (token) vectors in word2vec format")
    parser.add_argument('--save_t2v', dest='save_t2v', required=False,
                        help="save target vectors in word2vec format")
    parser.add_argument('--export_code_vectors', action='store_true', required=False,
                        help="export code vectors for the given examples")
    parser.add_argument('--release', action='store_true',
                        help='if specified and loading a trained models, release the loaded models for a lower models '
                             'size.')
    parser.add_argument('--predict', action='store_true')
    args = parser.parse_args(raw_args)
    config = Config.get_default_config(args)

    model = Model(config)
    # print('Created models')
    if config.TRAIN_PATH:
        model.train()
    if args.save_w2v is not None:
        model.save_word2vec_format(args.save_w2v, source=VocabType.Token)
        print('Origin word vectors saved in word2vec text format in: %s' % args.save_w2v)
    if args.save_t2v is not None:
        model.save_word2vec_format(args.save_t2v, source=VocabType.Target)
        print('Target word vectors saved in word2vec text format in: %s' % args.save_t2v)
    if config.TEST_PATH and not args.data_path:
        eval_results = model.evaluate()
        if eval_results is not None:
            results, precision, recall, f1 = eval_results
            print(results)
            print('Precision: ' + str(precision) + ', recall: ' + str(recall) + ', F1: ' + str(f1))
    if args.predict:
        predictor = InteractivePredictor(config, model)
        list_return = predictor.predict()
        return list_return
    model.close_session()


if __name__ == '__main__':
    main()
